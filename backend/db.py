import sqlite3
from datetime import datetime, timedelta
from config import DB_FILE
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            excerpt TEXT,
            publish_time TEXT,
            url TEXT UNIQUE,
            content TEXT,
            category TEXT,
            scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def article_exists(url):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM articles WHERE url = ?", (url,))
    count = cursor.fetchone()[0]
    conn.close()
    return count > 0

def insert_article(article):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO articles (title, excerpt, publish_time, url, content, category, scraped_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            article['title'],
            article['excerpt'],
            article['publish_time'],
            article['url'],
            article['content'],
            article['category'],
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))
        conn.commit()
        logging.info(f"Article saved (Category: {article['category']})")
    except sqlite3.IntegrityError:
        logging.warning("Article already exists in database, skipping.")
    finally:
        conn.close()

def delete_old_articles():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cutoff = datetime.now() - timedelta(hours=24)
    cutoff_str = cutoff.strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("DELETE FROM articles WHERE scraped_at < ?", (cutoff_str,))
    deleted_count = cursor.rowcount
    conn.commit()
    conn.close()
    logging.info(f"[−] Removed {deleted_count} old articles.")
