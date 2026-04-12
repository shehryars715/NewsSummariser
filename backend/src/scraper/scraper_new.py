import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone
from urllib.robotparser import RobotFileParser

from src.core.config import HEADERS, NEWS_SOURCES
from src.core.database import supabase
from src.scraper.sources import SOURCE_PARSERS
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
        "source": article_meta['source'],
    }

    try:
        response = supabase.table('news_articles').insert(article_data).execute()
        print(f"[✓] Article inserted: {article_meta['title']}{article_meta['category']} [{article_meta['source']}]")
    except Exception as e:
        print(f"[!] Failed to insert article: {e}")


def get_robot_parser(robots_url):
    response = requests.get(robots_url, headers=HEADERS, timeout=10)
    response.raise_for_status()

    parser = RobotFileParser()
    parser.set_url(robots_url)
    parser.parse(response.text.splitlines())
    return parser


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


def scrape_source(source_config, robot_parser):
    """Scrape articles from a single source."""
    source_name = source_config['name']
    display_name = source_config['display_name']
    base_url = source_config['base_url']
    parsers = SOURCE_PARSERS[source_name]

    print(f"\n{'='*50}")
    print(f"[→] Scraping {display_name} ({base_url})")
    print(f"{'='*50}")

    try:
        response = requests.get(base_url, headers=HEADERS, timeout=20)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
    except Exception as e:
        print(f"[!] Failed to fetch {display_name} listing page: {e}")
        return 0

    article_blocks = parsers['extract_links'](soup)
    print(f"[i] Found {len(article_blocks)} article links from {display_name}")

    new_count = 0
    for meta in article_blocks:
        if article_exists(meta['url']):
            continue

        if not robot_parser.can_fetch(HEADERS['User-Agent'], meta['url']):
            print(f"[=] Skipping blocked article: {meta['title'][:50]}")
            continue

        print(f"\n[→] Scraping: {meta['title'][:60]}...")
        human_delay()

        article_page = parsers['scrape_article'](meta['url'])
        meta['content'] = article_page['content']
        if meta['excerpt'] == 'N/A':
            meta['excerpt'] = article_page['excerpt']
        if meta['publish_time'] == 'N/A':
            meta['publish_time'] = article_page['publish_time']

        text_for_classification = f"{meta['title']} {meta['excerpt']}"
        meta['category'] = classify_category(text_for_classification)

        insert_article(meta)
        new_count += 1

    return new_count


def scrape_once():
    if not check_supabase_connection():
        print("[!] Scraping aborted due to database connection failure.")
        return

    print(f"\n[✓] Starting multi-source scrape at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    total_new = 0
    for source_config in NEWS_SOURCES:
        source_name = source_config['name']
        robots_url = source_config['robots_url']
        base_url = source_config['base_url']

        try:
            robot_parser = get_robot_parser(robots_url)
        except Exception as e:
            print(f"[!] Failed to fetch robots.txt for {source_config['display_name']}: {e}")
            continue

        if not robot_parser.can_fetch(HEADERS['User-Agent'], base_url):
            print(f"[!] Scraping blocked by robots.txt for {base_url}")
            continue

        try:
            new_count = scrape_source(source_config, robot_parser)
            total_new += new_count
            print(f"[+] {new_count} new article(s) from {source_config['display_name']}")
        except Exception as e:
            print(f"[!] Error scraping {source_config['display_name']}: {e}")
            continue

    if total_new == 0:
        print("\n[=] No new articles found across all sources.")
    else:
        print(f"\n[+] Total: {total_new} new article(s) added to DB across all sources.")
