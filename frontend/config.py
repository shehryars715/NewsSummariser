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


import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Supabase Configuration
    SUPABASE_URL = os.getenv('SUPABASE_URL')
    SUPABASE_KEY = os.getenv('SUPABASE_KEY')
    
    # Scraper Configuration
    USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    REQUEST_TIMEOUT = 30
    MAX_RETRIES = 3
    
    # News Sources
    NEWS_SOURCES = [
        {
            'name': 'BBC News',
            'url': 'https://www.bbc.com/news',
            'selectors': {
                'articles': 'div[data-entityid="container-top-stories#1"] a[href*="/news/"]',
                'title': 'h1, h2, h3',
                'content': 'article p, .story-body p',
                'published_at': 'time',
                'author': '[rel="author"], .byline'
            }
        },
        {
            'name': 'Reuters',
            'url': 'https://www.reuters.com/news/archive',
            'selectors': {
                'articles': 'article.story a[href*="/article/"]',
                'title': 'h1, h2',
                'content': 'article p',
                'published_at': 'time',
                'author': '.author-name'
            }
        }
    ]
    
    # Database Configuration
    DB_TABLE_NAME = 'news_articles'
    BATCH_SIZE = 50
    SCRAPE_INTERVAL_MINUTES = 30