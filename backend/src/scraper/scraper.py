import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, timezone

from src.core.config import BASE_URL, HEADERS
from src.core.database import supabase
from src.scraper.parser import extract_article_data, scrape_article_content
from src.scraper.classifier import classify_category
from src.utils.helpers import human_delay


def article_exists(article_url):
    """Checks if article already exists."""
    try:
        response = supabase.table('news_articles').select('id').eq('url', article_url).execute()
        return len(response.data) > 0
    except Exception as e:
        print(f"[!] Error checking article: {e}")
        return True


def insert_article(article_meta):
    raw_time = article_meta.get("publish_time")
    if not raw_time or raw_time in ["N/A", "", None]:
        publish_time = datetime.now(timezone.utc).isoformat()
    else:
        publish_time = raw_time

    article_data = {
        "title": article_meta['title'],
        "excerpt": article_meta['excerpt'],
        "publish_time": publish_time,
        "url": article_meta['url'],
        "content": article_meta['content'],
        "category": article_meta['category'],
    }

    try:
        response = supabase.table('news_articles').insert(article_data).execute()
        print(f"[✓] Article inserted: {article_meta['title']}{article_meta['category']}")
    except Exception as e:
        print(f"[!] Failed to insert article: {e}")


def delete_old_articles():
    try:
        cutoff_date = (datetime.now() - timedelta(days=1)).isoformat()
        response = (
            supabase.table("news_articles")
            .delete()
            .lt("scraped_at", cutoff_date)
            .execute()
        )
        deleted_count = len(response.data) if response.data else 0
        print(f"[+] Deleted {deleted_count} old article(s) from Supabase.")
    except Exception as e:
        print(f"[!] Error deleting old articles: {e}")


def get_latest_news_page():
    response = requests.get(BASE_URL, headers=HEADERS, timeout=10)
    response.raise_for_status()
    return BeautifulSoup(response.text, 'html.parser')


def check_supabase_connection():
    """Attempts a simple query to verify the connection to Supabase."""
    print("[ ] Attempting to connect to Supabase database...")
    try:
        response = supabase.table('news_articles').select("id", count="exact").limit(1).execute()
        print("[✓] Successfully connected to Supabase database.")
        print(f"[i] Found {response.count} total articles in the database.")
        return True
    except Exception as e:
        print(f"[!] Failed to connect to Supabase database: {e}")
        print(f"[!] Please check your SUPABASE_URL and SUPABASE_KEY environment variables.")
        return False


def scrape_once():
    if not check_supabase_connection():
        print("[!] Scraping aborted due to database connection failure.")
        return

    print(f"\n[✓] Checking for new articles at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    try:
        soup = get_latest_news_page()
    except Exception as e:
        print(f"[!] Failed to fetch main page: {e}")
        return

    article_blocks = soup.find_all('article', class_='story')
    new_count = 0

    for article in article_blocks:
        meta = extract_article_data(article)
        if not meta['url']:
            continue

        if article_exists(meta['url']):
            print(f"[=] Article already in database: {meta['title']}")
            continue

        print(f"\n[→] Scraping new article: {meta['title']}")
        print(f"URL: {meta['url']}")
        human_delay()

        content = scrape_article_content(meta['url'])
        meta['content'] = content

        text_for_classification = f"{meta['title']} {meta['excerpt']}"
        meta['category'] = classify_category(text_for_classification)

        insert_article(meta)
        new_count += 1

    if new_count == 0:
        print("[=] No new articles found.")
    else:
        print(f"[+] {new_count} new article(s) added to DB.")
