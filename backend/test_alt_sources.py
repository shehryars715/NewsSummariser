"""Test alternative Pakistani news sources."""
import requests
from bs4 import BeautifulSoup

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9'
}

# === THE NEWS INTERNATIONAL ===
print("=== THE NEWS INTERNATIONAL - LISTING ===")
try:
    r = requests.get("https://www.thenews.com.pk/latest-stories", headers=HEADERS, timeout=10)
    print(f"Status: {r.status_code}, Length: {len(r.text)}")
    soup = BeautifulSoup(r.text, "html.parser")
    print(f"Title: {soup.title.string if soup.title else 'None'}")
    
    news_links = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if "thenews.com.pk" in href and ("/latest/" in href or "/print/" in href or "/archive/" in href):
            txt = a.get_text(strip=True)
            if txt and len(txt) > 15:
                news_links.append((href, txt[:80]))
                if len(news_links) >= 5:
                    break
    
    if not news_links:
        # Try different patterns
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if "thenews.com.pk" in href:
                txt = a.get_text(strip=True)
                if txt and len(txt) > 30:
                    news_links.append((href, txt[:80]))
                    if len(news_links) >= 5:
                        break
    
    for url, title in news_links:
        print(f"  {title} -> {url}")
except Exception as e:
    print(f"Error: {e}")

# === ARY NEWS ===
print("\n=== ARY NEWS - LISTING ===")
try:
    r = requests.get("https://arynews.tv/latest-news/", headers=HEADERS, timeout=10)
    print(f"Status: {r.status_code}, Length: {len(r.text)}")
    soup = BeautifulSoup(r.text, "html.parser")
    print(f"Title: {soup.title.string if soup.title else 'None'}")
    
    news_links = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if "arynews.tv" in href and href.count("/") > 3:
            txt = a.get_text(strip=True)
            if txt and len(txt) > 25:
                news_links.append((href, txt[:80]))
                if len(news_links) >= 5:
                    break
    
    for url, title in news_links:
        print(f"  {title} -> {url}")
except Exception as e:
    print(f"Error: {e}")

# === BOL NEWS ===
print("\n=== BOL NEWS - LISTING ===")
try:
    r = requests.get("https://www.bolnews.com/latest/", headers=HEADERS, timeout=10)
    print(f"Status: {r.status_code}, Length: {len(r.text)}")
    soup = BeautifulSoup(r.text, "html.parser")
    print(f"Title: {soup.title.string if soup.title else 'None'}")
    
    news_links = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if "bolnews.com" in href:
            txt = a.get_text(strip=True)
            if txt and len(txt) > 25:
                news_links.append((href, txt[:80]))
                if len(news_links) >= 5:
                    break
    
    for url, title in news_links:
        print(f"  {title} -> {url}")
except Exception as e:
    print(f"Error: {e}")

print("\nDone!")
