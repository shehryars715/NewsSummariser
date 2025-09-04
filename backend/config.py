import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings



BASE_URL = "https://www.dawn.com/latest-news"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}
DB_FILE = "data/articles.db"
CHECK_INTERVAL = 7200  # 2 hours


# Load environment variables
load_dotenv()


# Gemini models
EMBEDDING_MODEL = "models/embedding-001"
CHAT_MODEL = "gemini-2.5-flash"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize Gemini Embeddings
embedding_model = GoogleGenerativeAIEmbeddings(
    model=EMBEDDING_MODEL,
    google_api_key=GEMINI_API_KEY
)
