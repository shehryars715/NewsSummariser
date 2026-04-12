import faiss
import numpy as np
import pickle
import io

from src.core.config import get_embedding_dimension, get_embedding_model
from src.core.database import supabase

BUCKET_NAME = "Faiss"
FAISS_FILE = "faiss_index.bin"
META_FILE = "metadata.pkl"


def fetch_articles():
    """Get all articles from database."""
    print("Fetching articles from database...")
    response = supabase.table('news_articles').select('id, title, excerpt, url, category, source').execute()
    print(f"Found {len(response.data)} articles")
    return response.data


def generate_embeddings(articles):
    """Create embeddings for title + excerpt."""
    embedding_model = get_embedding_model()
    if embedding_model is None:
        raise RuntimeError("Local embedding model is not configured")

    print("Generating embeddings...")
    texts, metadata = [], []

    for article in articles:
        text = f"{article['title']} {article['excerpt']}"
        texts.append(text)
        metadata.append(article)

    embeddings = embedding_model.embed_documents(texts)

    return np.array(embeddings, dtype=np.float32), metadata


def create_faiss_index(embeddings, metadata):
    """Create FAISS index and upload to Supabase storage."""
    print("Creating FAISS index...")

    embedding_dimension = get_embedding_dimension()
    if embedding_dimension is None:
        raise RuntimeError("Embedding dimension is not configured")

    index = faiss.IndexFlatL2(embedding_dimension)
    index.add(embeddings)

    faiss_bytes = bytes(faiss.serialize_index(index))

    meta_buffer = io.BytesIO()
    pickle.dump(metadata, meta_buffer)
    meta_buffer.seek(0)
    meta_bytes = meta_buffer.read()

    print("Uploading FAISS index to Supabase Storage...")
    supabase.storage.from_(BUCKET_NAME).update(FAISS_FILE, faiss_bytes)

    print("Uploading metadata to Supabase Storage...")
    supabase.storage.from_(BUCKET_NAME).update(META_FILE, meta_bytes)

    print(f"✅ Updated FAISS index with {index.ntotal} embeddings")
    return index


def faiss_create():
    """Main function to generate embeddings and upload FAISS index."""
    print("=== FAISS Embedding Generator ===")

    articles = fetch_articles()
    embeddings, metadata = generate_embeddings(articles)
    create_faiss_index(embeddings, metadata)
