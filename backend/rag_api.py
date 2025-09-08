from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
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
from supabase import create_client, Client
import tempfile


# Initialize Gemini LLM with modern syntax
llm = ChatGoogleGenerativeAI(
    model=CHAT_MODEL,
    api_key=GEMINI_API_KEY,  # Changed from google_api_key to api_key
    temperature=0.3
)

# Initialize Supabase client
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

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
    articles_used: List[ArticleSummary]  

class URLSummaryResponse(BaseModel):
    url: str
    title: str
    summary: str
    category: str

class URLSummaryRequest(BaseModel):
    url: str


def load_faiss_index():
    """Load FAISS index and metadata from Supabase Storage."""
    global faiss_index, metadata

    try:
        # Download FAISS index from Supabase Storage
        faiss_res = supabase.storage.from_("Faiss").download("faiss_index.bin")
        meta_res = supabase.storage.from_("Faiss").download("metadata.pkl")

        # Write to temp files (faiss.read_index only works on paths, not bytes)
        with tempfile.NamedTemporaryFile(delete=False) as faiss_tmp:
            faiss_tmp.write(faiss_res)
            faiss_tmp.flush()
            faiss_index = faiss.read_index(faiss_tmp.name)

        with tempfile.NamedTemporaryFile(delete=False) as meta_tmp:
            meta_tmp.write(meta_res)
            meta_tmp.flush()
            with open(meta_tmp.name, "rb") as f:
                metadata = pickle.load(f)

        print(f"✅ Loaded FAISS index from Supabase with {faiss_index.ntotal} articles")
        return True
    except Exception as e:
        print(f"❌ Error loading FAISS index: {e}")
        return False

def save_faiss_index():
    """Save FAISS index + metadata back to Supabase Storage."""
    try:
        # Save locally
        faiss.write_index(faiss_index, "faiss_index.bin")
        with open("metadata.pkl", "wb") as f:
            pickle.dump(metadata, f)

        # Upload (overwrite = upsert)
        supabase.storage.from_("Faiss").upload("faiss_index.bin", "faiss_index.bin", {"upsert": "true"})
        supabase.storage.from_("Faiss").upload("metadata.pkl", "metadata.pkl", {"upsert": "true"})

        print("✅ FAISS index + metadata saved to Supabase")
    except Exception as e:
        print(f"❌ Error saving FAISS index: {e}")


def get_article_by_url(article_url: str):
    """Retrieve article by URL from database."""
    try:
        response = supabase.table('news_articles').select('*').eq('url', article_url).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error fetching article by URL: {e}")
        return None


def generate_article_summary(article):
    """Generate summary for a specific article."""
    system_prompt = SystemMessagePromptTemplate.from_template("""
    You are an expert article summarizer. Create a concise, informative summary of the provided article.
    
    Guidelines:
    - Keep it 2-3 paragraphs (150-250 words)
    - Focus on the main points and key information
    - Use clear, journalistic style
    - Include important facts, dates, and figures
    - Don't add information not present in the article
    """)
    
    # Prepare article content
    content = f"Title: {article['title']}\n\nExcerpt: {article['excerpt']}\n\nFull Article:\n{article['content']}"
    
    human_prompt = HumanMessagePromptTemplate.from_template(f"""
    Please summarize this article:
    
    {content}
    """)
    system_message = system_prompt.format()
    human_message = human_prompt.format(
        title=article['title'],
        excerpt=article['excerpt'],
        content=article['content']
    )
    
    # Generate summary
    response = llm([system_message, human_message])
    return response.content

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
- Do not include unrelated content or mention anything like "article 1" or "the article above"
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
    response = llm.invoke(formatted_prompt)  
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or ["http://127.0.0.1:5500"] if serving HTML locally
    allow_credentials=True,
    allow_methods=["*"],   # Allow POST, GET, OPTIONS, etc.
    allow_headers=["*"],
)

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
    
@app.post("/summarize-url", response_model=URLSummaryResponse)
async def summarize_by_url(request: URLSummaryRequest):
    """Summarize a specific article by URL."""
    # Get article from database
    article = get_article_by_url(request.url)
    
    if not article:
        raise HTTPException(status_code=404, detail="Article not found in database")
    
    # Check if article has content
    if not article.get('content') or article['content'] == 'No content found.':
        raise HTTPException(status_code=400, detail="Article content is not available")
    
    try:
        # Generate summary
        summary = generate_article_summary(article)
        
        return URLSummaryResponse(
            url=article['url'],
            title=article['title'],
            summary=summary,
            category=article.get('category', 'Unknown')
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating summary: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    
    # Run the API
    uvicorn.run(app, host="0.0.0.0", port=port)