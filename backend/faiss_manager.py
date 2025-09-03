import os
import sqlite3
import logging
from langchain_community.vectorstores import FAISS
from langchain.schema import Document
from config import DB_FILE
from embeddings import embeddings

class FAISSManager:
    def __init__(self, store_path: str):
        self.store_path = store_path

    def _load_articles(self):
        """Fetch ALL articles from SQLite."""
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, excerpt, content, url, category FROM articles")
        rows = cursor.fetchall()
        conn.close()

        return [
            Document(
                page_content=f"{title}\n\n{excerpt}\n\n{content}",
                metadata={"id": _id, "url": url, "category": category},
            )
            for _id, title, excerpt, content, url, category in rows
        ]

    def rebuild(self):
        """Completely rebuild FAISS index from DB articles."""
        docs = self._load_articles()
        if not docs:
            logging.warning("No articles found in database.")
            return None

        # ✅ Build fresh FAISS index
        store = FAISS.from_documents(docs, embeddings)

        # ✅ Overwrite old index
        if os.path.exists(self.store_path):
            for f in os.listdir(self.store_path):
                os.remove(os.path.join(self.store_path, f))

        store.save_local(self.store_path)
        logging.info(f"FAISS index rebuilt at {self.store_path}")
        return store

    def load(self):
        """Load FAISS index if available, else rebuild it."""
        if os.path.exists(self.store_path):
            return FAISS.load_local(
                self.store_path,
                embeddings,
                allow_dangerous_deserialization=True,
            )
        else:
            return self.rebuild()

    def search(self, query: str, k: int = 5):
        store = self.load()
        if not store:
            return []
        return store.similarity_search(query, k=k)
