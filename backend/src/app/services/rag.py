import faiss
import numpy as np
import pickle
import tempfile

from fastapi import HTTPException

from src.core.config import get_embedding_model
from src.core.database import supabase

faiss_index = None
metadata = None


def load_faiss_index():
    """Load FAISS index and metadata from Supabase Storage."""
    global faiss_index, metadata

    try:
        faiss_res = supabase.storage.from_("Faiss").download("faiss_index.bin")
        meta_res = supabase.storage.from_("Faiss").download("metadata.pkl")

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


def retrieve_articles(query: str, k: int = 3):
    """Retrieve top k similar articles."""
    if faiss_index is None or metadata is None:
        raise HTTPException(status_code=500, detail="FAISS index not loaded")

    embedding_model = get_embedding_model()
    if embedding_model is None:
        raise HTTPException(status_code=500, detail="Local embedding model is not configured")

    query_embedding = embedding_model.embed_query(query)
    query_vector = np.array([query_embedding], dtype=np.float32)

    distances, indices = faiss_index.search(query_vector, k)

    articles = []
    for distance, idx in zip(distances[0], indices[0]):
        article = metadata[idx]
        articles.append({
            'title': article['title'],
            'excerpt': article['excerpt'],
            'url': article['url'],
            'category': article['category'],
            'relevance_score': float(1 / (1 + distance)),
        })

    return articles


def get_article_by_url(article_url: str):
    """Retrieve article by URL from database."""
    try:
        response = supabase.table('news_articles').select('*').eq('url', article_url).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error fetching article by URL: {e}")
        return None
