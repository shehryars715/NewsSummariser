"""Source-specific parsers for each news website."""
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup
from src.core.config import HEADERS


# ===================== GEO.TV =====================

def geo_extract_links(soup):
    """Extract article links from Geo.tv listing page."""
    seen_urls = set()
    articles = []

    for link in soup.find_all('a', href=True):
        href = link.get('href', '')
        absolute_url = urljoin("https://www.geo.tv/latest-news", href)
        parsed = urlparse(absolute_url)

        if parsed.netloc != 'www.geo.tv':
            continue
        if not parsed.path.startswith('/latest/'):
            continue
        if absolute_url in seen_urls:
            continue

        container = link.find_parent(['div', 'li'])
        time_tag = container.find('span', class_='date') if container else None
        title = " ".join(link.get_text(" ", strip=True).split()) or link.get('title', '').strip()

        if not title or len(title) < 5:
            continue

        seen_urls.add(absolute_url)
        articles.append({
            'title': title,
            'excerpt': 'N/A',
            'publish_time': time_tag.get_text(strip=True) if time_tag else 'N/A',
            'url': absolute_url,
            'source': 'geo',
        })

    return articles


def geo_scrape_article(url):
    """Scrape full article content from Geo.tv."""
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'html.parser')
        content_div = soup.select_one('div.story-area') or soup.select_one('div.content-area')

        if not content_div:
            return {'content': 'No content found.', 'excerpt': 'N/A', 'publish_time': 'N/A'}

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
        return {'content': f"Error fetching article: {e}", 'excerpt': 'N/A', 'publish_time': 'N/A'}


# ===================== EXPRESS TRIBUNE =====================

def tribune_extract_links(soup):
    """Extract article links from Express Tribune listing page."""
    seen_urls = set()
    articles = []

    for link in soup.find_all('a', href=True):
        href = link.get('href', '')
        if '/story/' not in href:
            continue

        absolute_url = href if href.startswith('http') else urljoin("https://tribune.com.pk", href)
        parsed = urlparse(absolute_url)

        if 'tribune.com.pk' not in parsed.netloc:
            continue
        if absolute_url in seen_urls:
            continue

        title = link.get_text(strip=True)

        if not title or len(title) < 10:
            continue

        seen_urls.add(absolute_url)
        articles.append({
            'title': title,
            'excerpt': 'N/A',
            'publish_time': 'N/A',
            'url': absolute_url,
            'source': 'tribune',
        })

    return articles


def tribune_scrape_article(url):
    """Scrape full article content from Express Tribune."""
    try:
        res = requests.get(url, headers=HEADERS, timeout=15)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'html.parser')

        # Tribune uses <p> tags inside div.story-text for article body
        story_text_divs = soup.select('div.story-text')
        paragraphs = []
        for div in story_text_divs:
            paragraphs.extend(div.find_all('p'))

        # Fallback: get from the main content area
        if not paragraphs:
            main = soup.select_one('div.storypage') or soup.select_one('div.maincontent-customwidth')
            if main:
                paragraphs = main.find_all('p')

        content = "\n".join(
            p.get_text(strip=True) for p in paragraphs
            if p.get_text(strip=True) and len(p.get_text(strip=True)) > 20
        )

        description_tag = soup.find('meta', attrs={'name': 'description'})
        excerpt = description_tag.get('content', 'N/A').strip() if description_tag else 'N/A'

        date_el = soup.select_one('div.story-date') or soup.select_one('span.story-date')
        publish_time = date_el.get_text(strip=True) if date_el else 'N/A'

        return {
            'content': content or 'No content found.',
            'excerpt': excerpt or 'N/A',
            'publish_time': publish_time or 'N/A',
        }
    except Exception as e:
        return {'content': f"Error fetching article: {e}", 'excerpt': 'N/A', 'publish_time': 'N/A'}


# ===================== THE NEWS INTERNATIONAL =====================

def thenews_extract_links(soup):
    """Extract article links from The News International listing page."""
    import re
    seen_urls = set()
    articles = []

    # TheNews article URLs follow pattern: /latest/{numeric_id}-{slug}
    article_pattern = re.compile(r'/latest/\d+-')

    for link in soup.find_all('a', href=True):
        href = link.get('href', '')
        absolute_url = href if href.startswith('http') else urljoin("https://www.thenews.com.pk", href)
        parsed = urlparse(absolute_url)

        if 'thenews.com.pk' not in parsed.netloc:
            continue
        if not article_pattern.search(parsed.path):
            continue
        if absolute_url in seen_urls:
            continue

        title = link.get_text(strip=True)

        if not title or len(title) < 10:
            continue

        seen_urls.add(absolute_url)
        articles.append({
            'title': title,
            'excerpt': 'N/A',
            'publish_time': 'N/A',
            'url': absolute_url,
            'source': 'thenews',
        })

    return articles


def thenews_scrape_article(url):
    """Scrape full article content from The News International."""
    try:
        res = requests.get(url, headers=HEADERS, timeout=15)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'html.parser')

        # The News uses div.story-detail for article body
        content_div = soup.select_one('div.story-detail')
        if not content_div:
            content_div = soup.select_one('div.detail-content')

        if not content_div:
            return {'content': 'No content found.', 'excerpt': 'N/A', 'publish_time': 'N/A'}

        paragraphs = content_div.find_all('p')
        content = "\n".join(
            p.get_text(strip=True) for p in paragraphs
            if p.get_text(strip=True) and len(p.get_text(strip=True)) > 20
        )

        if not content:
            content = " ".join(content_div.get_text(" ", strip=True).split())

        description_tag = soup.find('meta', attrs={'name': 'description'})
        excerpt = description_tag.get('content', 'N/A').strip() if description_tag else 'N/A'

        h1 = soup.find('h1')
        # Try to find date
        date_el = soup.select_one('span.detail-time') or soup.select_one('div.detail-date')
        publish_time = date_el.get_text(strip=True) if date_el else 'N/A'

        return {
            'content': content or 'No content found.',
            'excerpt': excerpt or 'N/A',
            'publish_time': publish_time or 'N/A',
        }
    except Exception as e:
        return {'content': f"Error fetching article: {e}", 'excerpt': 'N/A', 'publish_time': 'N/A'}


# ===================== REGISTRY =====================

SOURCE_PARSERS = {
    'geo': {
        'extract_links': geo_extract_links,
        'scrape_article': geo_scrape_article,
    },
    'tribune': {
        'extract_links': tribune_extract_links,
        'scrape_article': tribune_scrape_article,
    },
    'thenews': {
        'extract_links': thenews_extract_links,
        'scrape_article': thenews_scrape_article,
    },
}
