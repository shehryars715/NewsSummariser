"""Source-specific parsers for each news website — RSS-based metadata extraction."""
import re
import html
from xml.etree import ElementTree as ET

import requests
from bs4 import BeautifulSoup
from src.core.config import HEADERS


# ─────────────────── helpers ───────────────────

def _strip_html(raw: str) -> str:
    """Remove HTML tags and decode entities from a string."""
    return BeautifulSoup(raw, 'html.parser').get_text(separator=' ', strip=True)


def _cdata_text(element) -> str:
    """Return stripped text from an XML element, handling CDATA and entities."""
    if element is None:
        return 'N/A'
    text = (element.text or '').strip()
    text = html.unescape(text)
    return _strip_html(text) if '<' in text else text


# ─────────────────── RSS feed parsers ───────────────────

def parse_rss_feed(rss_url: str, source_name: str) -> list[dict]:
    """Fetch an RSS feed and return a list of article metadata dicts."""
    try:
        response = requests.get(rss_url, headers=HEADERS, timeout=20)
        response.raise_for_status()
    except Exception as e:
        print(f"[!] Failed to fetch RSS feed {rss_url}: {e}")
        return []

    # Strip any leading BOM / whitespace so ElementTree can parse
    content = response.content.lstrip(b'\xef\xbb\xbf').strip()

    try:
        root = ET.fromstring(content)
    except ET.ParseError as e:
        print(f"[!] Failed to parse RSS XML from {rss_url}: {e}")
        return []

    # Namespace map for content:encoded
    ns = {
        'content': 'http://purl.org/rss/1.0/modules/content/',
        'dc': 'http://purl.org/dc/elements/1.1/',
    }

    articles = []
    seen_urls = set()

    for item in root.iter('item'):
        url_el = item.find('link')
        # <link> in RSS is sometimes an empty tag with tail text
        url = (url_el.text or (url_el.tail or '')).strip() if url_el is not None else ''
        url = html.unescape(url).strip()

        if not url or url in seen_urls:
            continue
        seen_urls.add(url)

        title_el = item.find('title')
        title = _cdata_text(title_el)
        if not title or len(title) < 5:
            continue

        pub_date_el = item.find('pubDate')
        pub_date = _cdata_text(pub_date_el)

        desc_el = item.find('description')
        excerpt = _cdata_text(desc_el) if desc_el is not None else 'N/A'
        if len(excerpt) < 5:
            excerpt = 'N/A'

        # Tribune provides full article body in content:encoded
        content_encoded = item.find('content:encoded', ns)
        full_content = _strip_html(content_encoded.text or '') if content_encoded is not None else None

        articles.append({
            'title': title,
            'excerpt': excerpt,
            'publish_time': pub_date,
            'url': url,
            'source': source_name,
            # None means we still need to fetch the article page
            '_rss_content': full_content,
        })

    return articles


# ─────────────────── GEO.TV ───────────────────

GEO_RSS_URL = 'https://www.geo.tv/rss/1/1'


def geo_extract_links(_soup=None) -> list[dict]:
    """Return article metadata from Geo.tv RSS feed."""
    return parse_rss_feed(GEO_RSS_URL, 'geo')


def geo_scrape_article(url: str) -> dict:
    """Scrape full article content from Geo.tv."""
    try:
        res = requests.get(url, headers=HEADERS, timeout=15)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'html.parser')
        content_div = soup.select_one('div.story-area') or soup.select_one('div.content-area')

        if not content_div:
            return {'content': 'No content found.', 'excerpt': 'N/A', 'publish_time': 'N/A'}

        paragraphs = content_div.find_all('p')
        content = '\n'.join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))
        if not content:
            content = ' '.join(content_div.get_text(' ', strip=True).split())

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
        return {'content': f'Error fetching article: {e}', 'excerpt': 'N/A', 'publish_time': 'N/A'}


# ─────────────────── EXPRESS TRIBUNE ───────────────────

TRIBUNE_RSS_URL = 'https://tribune.com.pk/feed/pakistan'


def tribune_extract_links(_soup=None) -> list[dict]:
    """Return article metadata from Express Tribune RSS feed."""
    return parse_rss_feed(TRIBUNE_RSS_URL, 'tribune')


def tribune_scrape_article(url: str) -> dict:
    """
    Tribune RSS provides full content via content:encoded, so this is only called
    as a fallback when _rss_content is None.
    """
    try:
        res = requests.get(url, headers=HEADERS, timeout=20)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'html.parser')

        story_text_divs = soup.select('div.story-text')
        paragraphs = []
        for div in story_text_divs:
            paragraphs.extend(div.find_all('p'))

        if not paragraphs:
            main = soup.select_one('div.storypage') or soup.select_one('div.maincontent-customwidth')
            if main:
                paragraphs = main.find_all('p')

        content = '\n'.join(
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
        return {'content': f'Error fetching article: {e}', 'excerpt': 'N/A', 'publish_time': 'N/A'}


# ─────────────────── THE NEWS INTERNATIONAL ───────────────────

THENEWS_RSS_URL = 'https://www.thenews.com.pk/rss/1/1'


def thenews_extract_links(_soup=None) -> list[dict]:
    """Return article metadata from The News International RSS feed."""
    return parse_rss_feed(THENEWS_RSS_URL, 'thenews')


def thenews_scrape_article(url: str) -> dict:
    """Scrape full article content from The News International."""
    try:
        res = requests.get(url, headers=HEADERS, timeout=15)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'html.parser')

        content_div = (
            soup.select_one('div.story-detail')
            or soup.select_one('div.detail-content')
        )

        if not content_div:
            return {'content': 'No content found.', 'excerpt': 'N/A', 'publish_time': 'N/A'}

        paragraphs = content_div.find_all('p')
        content = '\n'.join(
            p.get_text(strip=True) for p in paragraphs
            if p.get_text(strip=True) and len(p.get_text(strip=True)) > 20
        )
        if not content:
            content = ' '.join(content_div.get_text(' ', strip=True).split())

        description_tag = soup.find('meta', attrs={'name': 'description'})
        excerpt = description_tag.get('content', 'N/A').strip() if description_tag else 'N/A'

        date_el = soup.select_one('span.detail-time') or soup.select_one('div.detail-date')
        publish_time = date_el.get_text(strip=True) if date_el else 'N/A'

        return {
            'content': content or 'No content found.',
            'excerpt': excerpt or 'N/A',
            'publish_time': publish_time or 'N/A',
        }
    except Exception as e:
        return {'content': f'Error fetching article: {e}', 'excerpt': 'N/A', 'publish_time': 'N/A'}


# ─────────────────── REGISTRY ───────────────────

SOURCE_PARSERS = {
    'geo': {
        'extract_links': geo_extract_links,
        'scrape_article': geo_scrape_article,
        'rss_url': GEO_RSS_URL,
    },
    'tribune': {
        'extract_links': tribune_extract_links,
        'scrape_article': tribune_scrape_article,
        'rss_url': TRIBUNE_RSS_URL,
    },
    'thenews': {
        'extract_links': thenews_extract_links,
        'scrape_article': thenews_scrape_article,
        'rss_url': THENEWS_RSS_URL,
    },
}
