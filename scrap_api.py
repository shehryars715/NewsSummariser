import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.dawn.com/latest-news"
HEADERS = {"User-Agent": "Mozilla/5.0"}

def scrape_articles(limit=10):
    """
    Scrape latest Dawn news articles.
    Returns a list of articles with: title, url, summary, category
    """
    response = requests.get(BASE_URL, headers=HEADERS, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    articles = []
    for idx, item in enumerate(soup.find_all("article", class_="story"), start=1):
        title_tag = item.find("h2")
        link_tag = title_tag.find("a") if title_tag else None
        excerpt_tag = item.find("div", class_="story__excerpt")

        if not title_tag or not link_tag:
            continue

        articles.append({
            "title": title_tag.get_text(strip=True),
            "url": link_tag["href"],
            "summary": excerpt_tag.get_text(strip=True) if excerpt_tag else "No summary",
            "category": "News"  # placeholder, can classify later
        })

        if idx >= limit:
            break

    return articles
