from supabase import create_client, Client
from config import Config
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self):
        self.supabase: Client = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)
        self.table_name = Config.DB_TABLE_NAME
    
    def create_table_if_not_exists(self):
        """Create the news articles table if it doesn't exist"""
        # This would typically be done via SQL migration files
        # For Supabase, you might want to create the table manually in the dashboard
        pass
    
    def insert_article(self, article: Dict[str, Any]) -> bool:
        """Insert a single article into the database"""
        try:
            result = self.supabase.table(self.table_name).insert(article).execute()
            return len(result.data) > 0
        except Exception as e:
            logger.error(f"Error inserting article: {e}")
            return False
    
    def insert_articles_batch(self, articles: List[Dict[str, Any]]) -> bool:
        """Insert multiple articles in a batch"""
        try:
            result = self.supabase.table(self.table_name).insert(articles).execute()
            return len(result.data) == len(articles)
        except Exception as e:
            logger.error(f"Error inserting batch: {e}")
            return False
    
    def article_exists(self, url: str) -> bool:
        """Check if an article already exists in the database"""
        try:
            result = self.supabase.table(self.table_name)\
                .select('id')\
                .eq('url', url)\
                .execute()
            return len(result.data) > 0
        except Exception as e:
            logger.error(f"Error checking article existence: {e}")
            return False
    
    def get_latest_articles(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get the latest articles from the database"""
        try:
            result = self.supabase.table(self.table_name)\
                .select('*')\
                .order('published_at', desc=True)\
                .limit(limit)\
                .execute()
            return result.data
        except Exception as e:
            logger.error(f"Error fetching latest articles: {e}")
            return []