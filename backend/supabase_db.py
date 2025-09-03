from supabase import create_client
import os

# ⚡ Load from environment or config
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://your-project-ref.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "your-service-role-key")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

TABLE_NAME = "articles"


def article_exists(url: str) -> bool:
    """Check if article with this URL already exists in Supabase."""
    response = supabase.table(TABLE_NAME).select("id").eq("url", url).execute()
    return bool(response.data)


def insert_article(article: dict):
    """Insert a new article into Supabase."""
    record = {
        "title": article.get("title"),
        "summary": article.get("excerpt") or article.get("summary") or "",
        "content": article.get("content") or "",
        "url": article.get("url"),
        "published_at": article.get("published_at") or None,
        "source": article.get("source") or "Unknown",
        "category": article.get("category") or "Uncategorized"
    }
    supabase.table(TABLE_NAME).insert(record).execute()


def delete_old_articles(days: int = 2):
    """Delete articles older than `days` days (optional)."""
    from datetime import datetime, timedelta
    cutoff = datetime.utcnow() - timedelta(days=days)
    supabase.table(TABLE_NAME).delete().lt("published_at", cutoff.isoformat()).execute()


def fetch_latest_articles(limit: int = 10):
    """Fetch latest articles from Supabase."""
    response = supabase.table(TABLE_NAME).select("*").order("published_at", desc=True).limit(limit).execute()
    return response.data
