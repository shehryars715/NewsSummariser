import os
import requests
from dotenv import load_dotenv

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")

if not HF_TOKEN:
    raise EnvironmentError("Hugging Face token not found. Please set HF_TOKEN in your .env file.")

API_URL = "https://router.huggingface.co/hf-inference/models/facebook/bart-large-mnli"
headers = {
    "Authorization": f"Bearer {HF_TOKEN}",
}

CATEGORIES = [
    "Technology and Innovation",
    "Corporate and Business News",
    "Sports and Athletics",
    "National News from Pakistan",
]


def classify_category(text):
    payload = {
        "inputs": text,
        "parameters": {
            "candidate_labels": CATEGORIES,
            "hypothesis_template": "This article is about {}.",
            "multi_class": False,
        },
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=120)
        response.raise_for_status()
        result = response.json()

        if "labels" in result and "scores" in result:
            top_label = result["labels"][0]
            top_score = result["scores"][0]

            if top_score < 0.3:
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
