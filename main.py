import time
from db import init_db, delete_old_articles
from scrap import scrape_once
from config import CHECK_INTERVAL

def main():
    init_db()
    while True:
        scrape_once()
        print(f"\n[⏳] Sleeping for {CHECK_INTERVAL // 3600} hours...\n")
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
