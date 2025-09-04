import faiss
import numpy as np
import pickle
import os
from supabase import create_client, Client
from dotenv import load_dotenv
from config import embedding_model

# Load environment variables
load_dotenv()

# Supabase setup
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# File paths
FAISS_INDEX_PATH = "data/faiss_index.bin"
METADATA_PATH = "data/metadata.pkl"

def fetch_articles():
    """Get all articles from database."""
    print("Fetching articles from database...")
    response = supabase.table('news_articles').select('id, title, excerpt, url, category').execute()
    print(f"Found {len(response.data)} articles")
    return response.data

def generate_embeddings(articles):
    """Create embeddings for title + excerpt."""
    print("Generating embeddings...")
    texts = []
    metadata = []
    
    for article in articles:
        # Combine title and excerpt
        text = f"{article['title']} {article['excerpt']}"
        texts.append(text)
        metadata.append(article)
    
    # Generate embeddings
    embeddings = []
    for i, text in enumerate(texts):
        if i % 10 == 0:  # Progress update
            print(f"Processing {i}/{len(texts)}")
        
        embedding = embedding_model.embed_query(text)
        embeddings.append(embedding)
    
    return np.array(embeddings, dtype=np.float32), metadata

def create_faiss_index(embeddings, metadata):
    """Create and save FAISS index."""
    print("Creating FAISS index...")
    
    # Create index (768 is Gemini embedding dimension)
    index = faiss.IndexFlatL2(768)
    index.add(embeddings)
    
    # Save index and metadata
    faiss.write_index(index, FAISS_INDEX_PATH)
    with open(METADATA_PATH, 'wb') as f:
        pickle.dump(metadata, f)
    
    print(f"Saved FAISS index with {index.ntotal} embeddings")
    return index


def faiss_create():
    """Main function to generate embeddings."""
    print("=== FAISS Embedding Generator ===")
    
    # Create data directory
    os.makedirs("data", exist_ok=True)
    print("Data directory ensured.")
    
    # Generate embeddings
    articles = fetch_articles()
    embeddings, metadata = generate_embeddings(articles)
    create_faiss_index(embeddings, metadata)
    

if __name__ == "__main__":
    faiss_create()