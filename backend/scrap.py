from bs4 import BeautifulSoup
import requests
from datetime import datetime
from config import BASE_URL, HEADERS
from db import article_exists, insert_article, delete_old_articles
from utils import extract_article_data, scrape_article_content, human_delay, classify_category

def get_latest_news_page():
    response = requests.get(BASE_URL, headers=HEADERS, timeout=10)
    response.raise_for_status()
    return BeautifulSoup(response.text, 'html.parser')

def scrape_once():
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

        insert_article(meta)
        new_count += 1

    if new_count == 0:
        print("[=] No new articles found.")
    else:
        print(f"[+] {new_count} new article(s) added to DB.")

    delete_old_articles()

