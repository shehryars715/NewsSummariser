import time
from db import init_db
from scrap import scrape_once
from config import CHECK_INTERVAL
from faiss_manager import FAISSManager

FAISS_STORE_PATH = "faiss_store"

def main():
    init_db()
    faiss_manager = FAISSManager(store_path=FAISS_STORE_PATH)

    while True:
        # ✅ Scrape and insert into DB
        new_count = scrape_once()
        print(f"[📰] Scraped {new_count} new articles.")

        # ✅ Rebuild FAISS from scratch after each scrape
        faiss_manager.rebuild()

        print(f"\n[⏳] Sleeping for {CHECK_INTERVAL // 60} minutes...\n")
        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()
