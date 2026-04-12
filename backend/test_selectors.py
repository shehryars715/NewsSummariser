"""Quick test to verify HTML selectors for Dawn and Tribune."""
import requests
from bs4 import BeautifulSoup

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9'
}

# === DAWN LISTING PAGE ===
print("=== DAWN LISTING PAGE ===")
r = requests.get("https://www.dawn.com/latest-news", headers=HEADERS, timeout=10)
soup = BeautifulSoup(r.text, "html.parser")

# Find article links
dawn_links = []
for a in soup.find_all("a", href=True):
    href = a["href"]
    if "/news/" in href and "www.dawn.com" in href:
        title = a.get_text(strip=True)
        if title and len(title) > 20:
            dawn_links.append((href, title[:80]))
            if len(dawn_links) >= 5:
                break

for url, title in dawn_links:
    print(f"  {title} -> {url}")

# === DAWN ARTICLE PAGE ===
print("\n=== DAWN ARTICLE PAGE ===")
r = requests.get("https://www.dawn.com/news/1991130", headers=HEADERS, timeout=10)
soup = BeautifulSoup(r.text, "html.parser")

for sel in ["article.story", "div.story__content", "div.template__main", "article", "div.story-detail"]:
    el = soup.select_one(sel)
    if el:
        ps = el.find_all("p")
        print(f"  {sel}: found with {len(ps)} paragraphs")
        if ps:
            print(f"    First p: {ps[0].get_text(strip=True)[:100]}")
    else:
        print(f"  {sel}: NOT found")

desc = soup.find("meta", attrs={"name": "description"})
if desc:
    print(f"  meta desc: {desc.get('content', '')[:100]}")

h2 = soup.find("h2", class_="story__title")
print(f"  story__title h2: {h2.get_text(strip=True)[:80] if h2 else 'NOT found'}")

# Try h1 instead
h1 = soup.find("h1")
print(f"  h1: {h1.get_text(strip=True)[:80] if h1 else 'NOT found'}")

time_tag = soup.find("time")
print(f"  time tag datetime: {time_tag.get('datetime') if time_tag else 'NOT found'}")

span_date = soup.find("span", class_="story__time")
print(f"  story__time span: {span_date.get_text(strip=True) if span_date else 'NOT found'}")

# === TRIBUNE LISTING PAGE ===
print("\n=== TRIBUNE LISTING PAGE ===")
r = requests.get("https://tribune.com.pk/latest", headers=HEADERS, timeout=10)
soup = BeautifulSoup(r.text, "html.parser")

trib_links = []
for a in soup.find_all("a", href=True):
    href = a["href"]
    if "/story/" in href and "tribune.com.pk" in href:
        title = a.get_text(strip=True)
        if title and len(title) > 15:
            trib_links.append((href, title[:80]))
            if len(trib_links) >= 5:
                break

for url, title in trib_links:
    print(f"  {title} -> {url}")

# === TRIBUNE ARTICLE PAGE ===
print("\n=== TRIBUNE ARTICLE PAGE ===")
r = requests.get("https://tribune.com.pk/story/2602418/irans-guards-will-view-military-vessels-approaching-strait-of-hormuz-as-ceasefire-breach", headers=HEADERS, timeout=10)
soup = BeautifulSoup(r.text, "html.parser")

for sel in ["div.story-description", "div.story__content", "article", "div.main-content", "div.story-content", "div.article-content"]:
    el = soup.select_one(sel)
    if el:
        ps = el.find_all("p")
        print(f"  {sel}: found with {len(ps)} paragraphs")
        if ps:
            print(f"    First p: {ps[0].get_text(strip=True)[:100]}")
    else:
        print(f"  {sel}: NOT found")

desc = soup.find("meta", attrs={"name": "description"})
if desc:
    print(f"  meta desc: {desc.get('content', '')[:100]}")

h1 = soup.find("h1")
print(f"  h1: {h1.get_text(strip=True)[:80] if h1 else 'NOT found'}")

# Check various time/date selectors
for sel in ["span.story-date", "span.date", "time", "div.story-date"]:
    el = soup.select_one(sel)
    if el:
        print(f"  {sel}: {el.get_text(strip=True)[:50]}")
        if el.get("datetime"):
            print(f"    datetime attr: {el.get('datetime')}")

print("\nDone!")
