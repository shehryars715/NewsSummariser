"""Dry-run test to verify all 3 source parsers work correctly."""
import sys
sys.path.insert(0, ".")

import requests
from bs4 import BeautifulSoup
from src.core.config import HEADERS, NEWS_SOURCES
from src.scraper.sources import SOURCE_PARSERS


def test_source(source_config):
    name = source_config['name']
    display = source_config['display_name']
    base_url = source_config['base_url']
    parsers = SOURCE_PARSERS[name]

    print(f"\n{'='*60}")
    print(f"Testing: {display} ({base_url})")
    print(f"{'='*60}")

    # 1. Fetch listing page
    try:
        r = requests.get(base_url, headers=HEADERS, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, 'html.parser')
        print(f"  [✓] Listing page fetched (status {r.status_code})")
    except Exception as e:
        print(f"  [✗] Failed to fetch listing: {e}")
        return

    # 2. Extract links
    articles = parsers['extract_links'](soup)
    print(f"  [✓] Extracted {len(articles)} article links")

    if not articles:
        print(f"  [✗] No articles found!")
        return

    # Show first 3
    for a in articles[:3]:
        print(f"      - {a['title'][:60]}")
        print(f"        URL: {a['url'][:80]}")
        print(f"        Source: {a['source']}")

    # 3. Test scraping one article
    test_article = articles[0]
    print(f"\n  Scraping first article: {test_article['title'][:50]}...")
    try:
        result = parsers['scrape_article'](test_article['url'])
        content_len = len(result['content'])
        print(f"  [✓] Content: {content_len} chars")
        print(f"      Excerpt: {result['excerpt'][:80]}...")
        print(f"      Publish time: {result['publish_time'][:50]}")
        if content_len < 50:
            print(f"  [!] Content seems too short: '{result['content']}'")
        else:
            print(f"      Content preview: {result['content'][:120]}...")
    except Exception as e:
        print(f"  [✗] Failed to scrape article: {e}")


if __name__ == "__main__":
    for source in NEWS_SOURCES:
        test_source(source)

    print(f"\n{'='*60}")
    print("All sources tested!")
    print(f"{'='*60}")
