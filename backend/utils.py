import time
import random
import requests
from bs4 import BeautifulSoup
from config import HEADERS
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")

if not HF_TOKEN:
    raise EnvironmentError("Hugging Face token not found. Please set HF_TOKEN in your .env file.")

API_URL = "https://router.huggingface.co/hf-inference/models/facebook/bart-large-mnli"
headers = {
    "Authorization": f"Bearer {HF_TOKEN}",
}

CATEGORIES = ["Technology and Innovation", "Corporate and Business News", "Sports and Athletics", "National News from Pakistan"]


def classify_category(text):
    payload = {
        "inputs": text,
        "parameters": {
            "candidate_labels": CATEGORIES,
            "hypothesis_template": "This article is about {}.",  # Improves context
            "multi_class": False  # Ensures single-label output
        }
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        result = response.json()

        if "labels" in result and "scores" in result:
            top_label = result["labels"][0]
            top_score = result["scores"][0]

            # Optional: log low confidence
            if top_score < 0.4:
                print(f"[!] Low confidence ({top_score:.2f}) for: {text[:60]}")
                return "Others"

            return top_label

        else:
            print(f"[!] Unexpected response format: {result}")
            return "uncategorized"

    except requests.exceptions.Timeout:
        print("[!] Request timed out.")
        return "uncategorized"

    except requests.exceptions.RequestException as e:
        print(f"[!] HTTP Error: {e}")
        return "uncategorized"

    except Exception as e:
        print(f"[!] Unexpected error: {e}")
        return "uncategorized"



def extract_article_data(article):
    title_tag = article.find('h2', class_='story__title')
    excerpt_tag = article.find('div', class_='story__excerpt')
    time_tag = article.find('span', class_='timestamp--time')
    link_tag = title_tag.find('a') if title_tag else None

    return {
        'title': title_tag.get_text(strip=True) if title_tag else 'N/A',
        'excerpt': excerpt_tag.get_text(strip=True) if excerpt_tag else 'N/A',
        'publish_time': time_tag.get('title') if time_tag else 'N/A',
        'url': link_tag['href'] if link_tag else None
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

def human_delay(min_seconds=2, max_seconds=4):
    sleep_time = random.uniform(min_seconds, max_seconds)
    print(f"[...] Waiting {sleep_time:.2f} seconds")
    time.sleep(sleep_time)