from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup
from src.core.config import HEADERS


def normalize_article_url(href):
    absolute_url = urljoin("https://www.geo.tv/latest-news", href)
    parsed_url = urlparse(absolute_url)

    if parsed_url.netloc != 'www.geo.tv':
        return None

    if not parsed_url.path.startswith('/latest/'):
        return None

    return absolute_url


def extract_article_data(link):
    article_url = normalize_article_url(link.get('href'))
    container = link.find_parent(['div', 'li'])
    time_tag = container.find('span', class_='date') if container else None
    title = " ".join(link.get_text(" ", strip=True).split()) or link.get('title', '').strip()

    return {
        'title': title or 'N/A',
        'excerpt': 'N/A',
        'publish_time': time_tag.get_text(strip=True) if time_tag else 'N/A',
        'url': article_url,
    }


def scrape_article_content(url):
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'html.parser')
        content_div = soup.select_one('div.story-area') or soup.select_one('div.content-area')

        if not content_div:
            return {
                'content': 'No content found.',
                'excerpt': 'N/A',
                'publish_time': 'N/A',
            }

        paragraphs = content_div.find_all('p')
        content = "\n".join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))

        if not content:
            content = " ".join(content_div.get_text(" ", strip=True).split())

        description_tag = soup.find('meta', attrs={'name': 'description'})
        excerpt = description_tag.get('content', 'N/A').strip() if description_tag else 'N/A'
        publish_tag = soup.find('p', class_='post-date-time')
        publish_time = publish_tag.get_text(strip=True) if publish_tag else 'N/A'

        return {
            'content': content or 'No content found.',
            'excerpt': excerpt or 'N/A',
            'publish_time': publish_time or 'N/A',
        }

    except Exception as e:
        return {
            'content': f"Error fetching article: {e}",
            'excerpt': 'N/A',
            'publish_time': 'N/A',
        }
