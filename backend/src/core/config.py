import os
from dotenv import load_dotenv

try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    SentenceTransformer = None

load_dotenv()

# Scraper settings
BASE_URL = "https://www.geo.tv/latest-news"
ROBOTS_URL = "https://www.geo.tv/robots.txt"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9'
}
CHECK_INTERVAL = 7200  # 2 hours

# Multi-source configuration
NEWS_SOURCES = [
    {
        "name": "geo",
        "display_name": "Geo.tv",
        "base_url": "https://www.geo.tv/latest-news",
        "robots_url": "https://www.geo.tv/robots.txt",
        "domain": "www.geo.tv",
    },
    {
        "name": "tribune",
        "display_name": "Express Tribune",
        "base_url": "https://tribune.com.pk/latest",
        "robots_url": "https://tribune.com.pk/robots.txt",
        "domain": "tribune.com.pk",
    },
    {
        "name": "thenews",
        "display_name": "The News International",
        "base_url": "https://www.thenews.com.pk/latest-stories",
        "robots_url": "https://www.thenews.com.pk/robots.txt",
        "domain": "www.thenews.com.pk",
    },
]

# Models
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "BAAI/bge-base-en-v1.5")
CHAT_MODEL = "gemini-2.5-flash"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize local embeddings lazily so unrelated imports do not trigger model load
embedding_model = None
EMBEDDING_DIMENSION = None


class LocalEmbeddingModel:
    def __init__(self, model_name: str):
        self.client = SentenceTransformer(model_name)
        self.dimension = self.client.get_sentence_embedding_dimension()

    def embed_documents(self, texts):
        embeddings = self.client.encode(
            texts,
            normalize_embeddings=True,
            convert_to_numpy=True,
        )
        return embeddings.tolist()

    def embed_query(self, text):
        embedding = self.client.encode(
            text,
            normalize_embeddings=True,
            convert_to_numpy=True,
        )
        return embedding.tolist()


def get_embedding_model():
    global embedding_model, EMBEDDING_DIMENSION

    if embedding_model is not None:
        return embedding_model

    if SentenceTransformer is None:
        return None

    embedding_model = LocalEmbeddingModel(EMBEDDING_MODEL)
    EMBEDDING_DIMENSION = embedding_model.dimension
    return embedding_model


def get_embedding_dimension():
    model = get_embedding_model()
    if model is None:
        return None
    return EMBEDDING_DIMENSION
