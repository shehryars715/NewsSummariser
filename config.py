import os
from dotenv import load_dotenv

BASE_URL = "https://www.dawn.com/latest-news"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}
DB_FILE = "data/articles.db"
CHECK_INTERVAL = 7200  # 2 hours


# Load environment variables
load_dotenv()

DB_FILE = "data/articles.db"
FAISS_STORE_PATH = "faiss_store"

# Gemini models
EMBEDDING_MODEL = "models/embedding-001"
CHAT_MODEL = "gemini-2.5-flash"
