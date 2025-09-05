import faiss
import numpy as np
import pickle
import os
import io
from supabase import create_client, Client
from dotenv import load_dotenv
from config import embedding_model

# Load environment variables
load_dotenv()

# Supabase setup
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Storage bucket name (make sure this bucket exists in Supabase)
BUCKET_NAME = "Faiss"
FAISS_FILE = "faiss_index.bin"
META_FILE = "metadata.pkl"

def fetch_articles():
    """Get all articles from database."""
    print("Fetching articles from database...")
    response = supabase.table('news_articles').select('id, title, excerpt, url, category').execute()
    print(f"Found {len(response.data)} articles")
    return response.data

def generate_embeddings(articles):
    """Create embeddings for title + excerpt."""
    print("Generating embeddings...")
    texts, metadata = [], []
    
    for article in articles:
        text = f"{article['title']} {article['excerpt']}"
        texts.append(text)
        metadata.append(article)
    
    embeddings = []
    for i, text in enumerate(texts):
        if i % 10 == 0:
            print(f"Processing {i}/{len(texts)}")
        embedding = embedding_model.embed_query(text)
        embeddings.append(embedding)
    
    return np.array(embeddings, dtype=np.float32), metadata

def create_faiss_index(embeddings, metadata):
    """Create FAISS index and upload to Supabase storage (overwrite old files)."""
    print("Creating FAISS index...")
    
    # Create FAISS index
    index = faiss.IndexFlatL2(768)
    index.add(embeddings)
    
    # Serialize FAISS index to bytes
    faiss_bytes = bytes(faiss.serialize_index(index))
    
    # Serialize metadata to bytes
    meta_buffer = io.BytesIO()
    pickle.dump(metadata, meta_buffer)
    meta_buffer.seek(0)
    meta_bytes = meta_buffer.read()
    
    # Upload FAISS index (replace old file)
    print("Uploading FAISS index to Supabase Storage...")
    supabase.storage.from_(BUCKET_NAME).update(FAISS_FILE, faiss_bytes)
    
    # Upload metadata (replace old file)
    print("Uploading metadata to Supabase Storage...")
    supabase.storage.from_(BUCKET_NAME).update(META_FILE, meta_bytes)
    
    print(f"✅ Updated FAISS index with {index.ntotal} embeddings")
    return index


def faiss_create():
    """Main function to generate embeddings and upload FAISS index."""
    print("=== FAISS Embedding Generator ===")
    
    # Fetch articles & generate embeddings
    articles = fetch_articles()
    embeddings, metadata = generate_embeddings(articles)
    
    # Create FAISS index and upload
    create_faiss_index(embeddings, metadata)

if __name__ == "__main__":
    faiss_create()
