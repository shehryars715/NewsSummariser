import time
import requests
from bs4 import BeautifulSoup
from src.core.config import HEADERS


def extract_article_data(article):
    title_tag = article.find('h2', class_='story__title')
    excerpt_tag = article.find('div', class_='story__excerpt')
    time_tag = article.find('span', class_='timestamp--time')
    link_tag = title_tag.find('a') if title_tag else None

    return {
        'title': title_tag.get_text(strip=True) if title_tag else 'N/A',
        'excerpt': excerpt_tag.get_text(strip=True) if excerpt_tag else 'N/A',
        'publish_time': time_tag.get('title') if time_tag else 'N/A',
        'url': link_tag['href'] if link_tag else None,
    }


def scrape_article_content(url):
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        if res.status_code != 200:
            print(f"Retrying {url} after denial...")
            time.sleep(5)
            res = requests.get(url, headers=HEADERS, timeout=10)

        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'html.parser')
        content_div = soup.find('div', class_='story__content')

        if not content_div:
            return "No content found."

        paragraphs = content_div.find_all('p')
        return "\n".join(p.get_text(strip=True) for p in paragraphs)

    except Exception as e:
        return f"Error fetching article: {e}"
