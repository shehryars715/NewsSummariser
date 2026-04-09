import time
import random
from src.core.config import embedding_model


def generate_embedding(text):
    """Generates a single embedding for combined title + content."""
    try:
        return embedding_model.embed_query(text)
    except Exception as e:
        print(f"[!] Error generating embedding: {e}")
        return []


def human_delay(min_seconds=2, max_seconds=4):
    sleep_time = random.uniform(min_seconds, max_seconds)
    print(f"[...] Waiting {sleep_time:.2f} seconds")
    time.sleep(sleep_time)
