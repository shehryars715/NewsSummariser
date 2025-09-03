import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.dawn.com/latest-news"

def fetch_latest_news(limit=5):
    """Scrape latest news headlines from Dawn"""
    response = requests.get(BASE_URL, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    articles = soup.find_all("article", class_="story", limit=limit)

    news_list = []
    for article in articles:
        title = article.find("h2", class_="story__title")
        link = article.find("a", href=True)
        excerpt = article.find("div", class_="story__excerpt")

        news_list.append({
            "title": title.get_text(strip=True) if title else "No title",
            "url": link["href"] if link else None,
            "excerpt": excerpt.get_text(strip=True) if excerpt else None
        })
    return news_list
