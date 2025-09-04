from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import faiss
import numpy as np
import pickle
from langchain_google_genai import ChatGoogleGenerativeAI  
from contextlib import asynccontextmanager
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate  # Modern prompt handling
from config import embedding_model, GEMINI_API_KEY, CHAT_MODEL
import os
from typing import List


# Initialize Gemini LLM with modern syntax
llm = ChatGoogleGenerativeAI(
    model=CHAT_MODEL,
    api_key=GEMINI_API_KEY,  # Changed from google_api_key to api_key
    temperature=0.3
)

# Global variables for FAISS index
faiss_index = None
metadata = None

class QueryRequest(BaseModel):
    query: str
    max_articles: int = 3

class ArticleSummary(BaseModel):
    title: str
    excerpt: str
    url: str
    category: str
    relevance_score: float

class RAGResponse(BaseModel):
    query: str
    summary: str
    articles_used: List[ArticleSummary]  # Use capital List for type hints

def load_faiss_index():
    """Load FAISS index and metadata on startup."""
    global faiss_index, metadata
    
    try:
        faiss_index = faiss.read_index("data/faiss_index.bin")
        with open("data/metadata.pkl", 'rb') as f:
            metadata = pickle.load(f)
        print(f"Loaded FAISS index with {faiss_index.ntotal} articles")
        return True
    except Exception as e:
        print(f"Error loading FAISS index: {e}")
        return False

def retrieve_articles(query: str, k: int = 3):
    """Retrieve top k similar articles."""
    if faiss_index is None or metadata is None:
        raise HTTPException(status_code=500, detail="FAISS index not loaded")
    
    # Generate query embedding
    query_embedding = embedding_model.embed_query(query)
    query_vector = np.array([query_embedding], dtype=np.float32)
    
    # Search FAISS index
    distances, indices = faiss_index.search(query_vector, k)
    
    # Prepare articles
    articles = []
    for distance, idx in zip(distances[0], indices[0]):
        article = metadata[idx]
        articles.append({
            'title': article['title'],
            'excerpt': article['excerpt'],
            'url': article['url'],
            'category': article['category'],
            'relevance_score': float(1 / (1 + distance))
        })
    
    return articles

def generate_summary(query: str, articles: list):
    """Generate summary using Gemini LLM with modern prompt templates."""
    
    # Prepare context from articles
    context = "\n\n".join([
        f"Article {i+1}: {article['title']}\n{article['excerpt']}"
        for i, article in enumerate(articles)
    ])
    
    # Create prompt template using modern approach
    system_template = """
    You are a news summarization expert. Your task is to generate a clear and concise summary that answers the user's query, using only the most relevant and accurate information from the provided articles.

Guidelines:
- Only use information from the relevant articles
- Do not include unrelated content
- If the information is limited, explain that clearly
- Be objective, factual, and long (4-5 paragraphs)
- Maintain a journalistic tone
- Just give summary according to the query, do not add any additional information like "As an AI language model" or "Based on the articles provided"
    """
    
    human_template = """
    Query: {query}
    
    Articles:
    {context}
    
    Please provide a summary that answers the query based on these articles.
    """
    
    # Build the prompt
    prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(system_template),
        HumanMessagePromptTemplate.from_template(human_template)
    ])
    
    # Format the prompt with variables
    formatted_prompt = prompt.format_messages(
        query=query,
        context=context
    )
    
    # Generate response
    response = llm.invoke(formatted_prompt)  # Use invoke() instead of direct call
    return response.content

@asynccontextmanager
async def lifespan(app: FastAPI):
    if not load_faiss_index():
        print("Warning: FAISS index not loaded. API will not work properly.")
    yield  # Startup code runs before this, shutdown code can go after

# Initialize FastAPI
app = FastAPI(
    title="News RAG API",
    description="Retrieve and Generate summaries from news articles",
    lifespan=lifespan
)

@app.get("/")
async def root():
    """Health check endpoint."""
    return {"message": "News RAG API is running", "status": "healthy"}

@app.get("/stats")
async def get_stats():
    """Get index statistics."""
    if faiss_index is None or metadata is None:
        raise HTTPException(status_code=500, detail="FAISS index not loaded")
    
    # Count categories
    categories = {}
    for article in metadata:
        cat = article.get('category', 'Unknown')
        categories[cat] = categories.get(cat, 0) + 1
    
    return {
        "total_articles": len(metadata),
        "categories": categories,
        "index_dimension": faiss_index.d
    }

@app.post("/query", response_model=RAGResponse)
async def query_articles(request: QueryRequest):
    """Main RAG endpoint - retrieve articles and generate summary."""
    try:
        # Retrieve relevant articles
        articles = retrieve_articles(request.query, request.max_articles)
        
        if not articles:
            raise HTTPException(status_code=404, detail="No relevant articles found")
        
        # Generate summary
        summary = generate_summary(request.query, articles)
        
        # Prepare response
        articles_used = [ArticleSummary(**article) for article in articles]
        
        return RAGResponse(
            query=request.query,
            summary=summary,
            articles_used=articles_used
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

@app.post("/search")
async def search_articles(request: QueryRequest):
    """Search for articles without generating summary."""
    try:
        articles = retrieve_articles(request.query, request.max_articles)
        return {
            "query": request.query,
            "articles": [ArticleSummary(**article) for article in articles]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching articles: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    
    # Check if FAISS index exists
    if not os.path.exists("data/faiss_index.bin"):
        print("Error: FAISS index not found. Please run generate_faiss_embeddings.py first.")
        exit(1)
    
    # Run the API
    uvicorn.run(app, host="0.0.0.0", port=8000)