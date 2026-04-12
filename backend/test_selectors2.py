"""Deep selector debugging for Dawn and Tribune."""
import requests
from bs4 import BeautifulSoup

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9'
}

# === DAWN DEEP CHECK ===
print("=== DAWN DEBUG ===")
r = requests.get("https://www.dawn.com/news/1991130", headers=HEADERS, timeout=10)
print(f"Status: {r.status_code}, Length: {len(r.text)}")
soup = BeautifulSoup(r.text, "html.parser")

# Check title tag
print(f"Page title: {soup.title.string if soup.title else 'None'}")

# Check all divs with class
all_divs = soup.find_all("div", class_=True)
classes_found = set()
for d in all_divs:
    for c in d.get("class", []):
        if "story" in c.lower() or "content" in c.lower() or "article" in c.lower():
            classes_found.add(c)
print(f"Story/Content/Article div classes: {classes_found}")

# Find all paragraphs
all_p = soup.find_all("p")
print(f"Total <p> tags: {len(all_p)}")
for p in all_p[:5]:
    txt = p.get_text(strip=True)
    if len(txt) > 30:
        print(f"  p: {txt[:120]}")

# Check if it's JS-rendered
scripts = soup.find_all("script")
print(f"Script tags: {len(scripts)}")

# Try dawn listing page with different approach
print("\n=== DAWN LISTING DEBUG ===")
r = requests.get("https://www.dawn.com/latest-news", headers=HEADERS, timeout=10)
print(f"Status: {r.status_code}, Length: {len(r.text)}")
soup = BeautifulSoup(r.text, "html.parser")

all_links = soup.find_all("a", href=True)
print(f"Total links: {len(all_links)}")

# Show first 10 that contain /news/
news_links = [a for a in all_links if "/news/" in a.get("href", "")]
print(f"Links with /news/: {len(news_links)}")
for a in news_links[:5]:
    href = a["href"]
    txt = a.get_text(strip=True)[:60]
    print(f"  {txt} -> {href}")

# Check what's special
h2_tags = soup.find_all("h2")
print(f"\nTotal h2 tags: {len(h2_tags)}")
for h in h2_tags[:5]:
    parent_class = h.parent.get("class", []) if h.parent else []
    print(f"  h2: {h.get_text(strip=True)[:60]} (parent: {parent_class})")

# === TRIBUNE DEEP CHECK ===
print("\n=== TRIBUNE ARTICLE DEBUG ===")
r = requests.get("https://tribune.com.pk/story/2602418/irans-guards-will-view-military-vessels-approaching-strait-of-hormuz-as-ceasefire-breach", headers=HEADERS, timeout=10)
soup = BeautifulSoup(r.text, "html.parser")

# Check all content-related divs
for d in soup.find_all("div", class_=True):
    classes = d.get("class", [])
    for c in classes:
        if "story" in c.lower() or "content" in c.lower() or "article" in c.lower() or "body" in c.lower():
            ps = d.find_all("p")
            txt_len = len(d.get_text(strip=True))
            if txt_len > 100:
                print(f"  div.{c}: {len(ps)} <p> tags, {txt_len} chars text")
                if ps:
                    print(f"    First p: {ps[0].get_text(strip=True)[:100]}")

# All paragraphs with substantial text
print("\nSubstantial <p> tags in Tribune article:")
for p in soup.find_all("p"):
    txt = p.get_text(strip=True)
    if len(txt) > 50:
        parent_class = p.parent.get("class", []) if p.parent else []
        print(f"  [{parent_class}] {txt[:120]}")

print("\nDone!")
