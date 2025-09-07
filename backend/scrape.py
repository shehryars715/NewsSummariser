from bs4 import BeautifulSoup
import requests
import os
from datetime import datetime, timedelta
from config import BASE_URL, HEADERS
from utils import extract_article_data, scrape_article_content, human_delay, classify_category
from supabase import create_client, Client
from dotenv import load_dotenv
from datetime import timezone

# Load environment variables from .env file
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Initialize the Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)




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
        publish_time = datetime.now(timezone.utc).isoformat()  # always valid
    else:
        publish_time = raw_time  # assume scraper already gave ISO8601 string


    # Prepare data
    article_data = {
        "title": article_meta['title'],
        "excerpt": article_meta['excerpt'],
        "publish_time": publish_time,
        "url": article_meta['url'],
        "content": article_meta['content'],
        "category": article_meta['category']}
    
    try:
        response = supabase.table('news_articles').insert(article_data).execute()
        print(f"[✓] Article inserted: {article_meta['title']}{article_meta['category']}")
    except Exception as e:
        print(f"[!] Failed to insert article: {e}")


from datetime import datetime, timedelta

def delete_old_articles():
    try:
        # Calculate the cutoff datetime (1 days ago)
        cutoff_date = (datetime.now() - timedelta(days=1)).isoformat()

        # Delete rows where scraped_at < cutoff_date
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

        # 🔥 Classify article category (use title + excerpt + content)
        text_for_classification = f"{meta['title']} {meta['excerpt']}"
        meta['category'] = classify_category(text_for_classification)

        insert_article(meta) # This now calls the Supabase function
        new_count += 1

    if new_count == 0:
        print("[=] No new articles found.")
    else:
        print(f"[+] {new_count} new article(s) added to DB.")


# Initialize the Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- NEW: DATABASE CONNECTION CHECK FUNCTION ---
def check_supabase_connection():
    """
    Attempts a simple query to verify the connection to Supabase is working.
    """
    print("[ ] Attempting to connect to Supabase database...")
    try:
        # Try a simple, low-cost query (e.g., get the count of records)
        response = supabase.table('news_articles').select("id", count="exact").limit(1).execute()
        # If no exception is raised, the connection is successful
        print("[✓] Successfully connected to Supabase database.")
        print(f"[i] Found {response.count} total articles in the database.")
        return True
    except Exception as e:
        # This will catch connection errors, invalid credentials, etc.
        print(f"[!] Failed to connect to Supabase database: {e}")
        print(f"[!] Please check your SUPABASE_URL and SUPABASE_KEY in config_supabase.py")
        return False


