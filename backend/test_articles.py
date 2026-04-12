"""Test article page selectors for TheNews and Tribune."""
import requests
from bs4 import BeautifulSoup

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9'
}

# ===================== THE NEWS =====================
print("=== THE NEWS LISTING PAGE - link patterns ===")
r = requests.get("https://www.thenews.com.pk/latest-stories", headers=HEADERS, timeout=10)
soup = BeautifulSoup(r.text, "html.parser")

# Find links with /latest/ pattern
links = set()
for a in soup.find_all("a", href=True):
    href = a["href"]
    if "/latest/" in href and "thenews.com.pk" in href:
        links.add(href)

print(f"Total /latest/ links: {len(links)}")
sample_link = sorted(links)[0] if links else None
if sample_link:
    print(f"Sample: {sample_link}")

# Also check for pakistan/national/world patterns
for pat in ["/pakistan/", "/national/", "/world/", "/business/", "/sports/"]:
    plinks = [a["href"] for a in soup.find_all("a", href=True) if pat in a["href"]]
    if plinks:
        print(f"Links with {pat}: {len(plinks)}, e.g. {plinks[0][:80]}")

print("\n=== THE NEWS ARTICLE PAGE ===")
if sample_link:
    r = requests.get(sample_link, headers=HEADERS, timeout=10)
    print(f"Status: {r.status_code}")
    soup = BeautifulSoup(r.text, "html.parser")
    
    # Find content divs
    for d in soup.find_all("div", class_=True):
        classes = d.get("class", [])
        for c in classes:
            if "story" in c.lower() or "content" in c.lower() or "article" in c.lower() or "detail" in c.lower():
                ps = d.find_all("p")
                txt_len = len(d.get_text(strip=True))
                if txt_len > 200:
                    print(f"  div.{c}: {len(ps)} <p> tags, {txt_len} chars")
                    if ps:
                        print(f"    First p: {ps[0].get_text(strip=True)[:100]}")
    
    desc = soup.find("meta", attrs={"name": "description"})
    if desc:
        print(f"  meta description: {desc.get('content', '')[:100]}")
    
    h1 = soup.find("h1")
    if h1:
        print(f"  h1: {h1.get_text(strip=True)[:80]}")
    
    # Find date/time
    for sel in ["span.detail-time", "div.detail-date", "span.date", "time"]:
        el = soup.select_one(sel)
        if el:
            print(f"  {sel}: {el.get_text(strip=True)[:50]}")

# ===================== TRIBUNE =====================
print("\n=== TRIBUNE LISTING - link patterns ===")
r = requests.get("https://tribune.com.pk/latest", headers=HEADERS, timeout=10)
soup = BeautifulSoup(r.text, "html.parser")

links = set()
for a in soup.find_all("a", href=True):
    href = a["href"]
    if "/story/" in href and "tribune.com.pk" in href:
        links.add(href)

print(f"Total /story/ links: {len(links)}")

# Get a not-opinion article
sample = None
for lnk in sorted(links):
    if "opinion" not in lnk and "blog" not in lnk:
        sample = lnk
        break

if sample:
    print(f"Sample: {sample}")
    print("\n=== TRIBUNE ARTICLE PAGE ===")
    r = requests.get(sample, headers=HEADERS, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")
    
    # The content is in p tags with parent class story-text
    story_ps = soup.select("div.story-text p")
    print(f"  div.story-text p: {len(story_ps)} paragraphs")
    for p in story_ps[:3]:
        txt = p.get_text(strip=True)
        if txt:
            print(f"    {txt[:120]}")
    
    # storypage
    storypage = soup.select_one("div.storypage")
    if storypage:
        all_story_text = storypage.select("div.story-text")
        print(f"  div.storypage > div.story-text elements: {len(all_story_text)}")
    
    desc = soup.find("meta", attrs={"name": "description"})
    if desc:
        print(f"  meta description: {desc.get('content', '')[:100]}")
    
    h1 = soup.find("h1")
    if h1:
        print(f"  h1: {h1.get_text(strip=True)[:80]}")
    
    date_span = soup.select_one("div.story-date") or soup.select_one("span.story-date")
    if date_span:
        print(f"  date: {date_span.get_text(strip=True)[:50]}")

print("\nDone!")
