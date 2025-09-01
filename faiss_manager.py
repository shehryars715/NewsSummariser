import os
import sqlite3
import logging
from langchain_community.vectorstores import FAISS
from langchain.schema import Document
from config import DB_FILE


class FAISSManager:
    def __init__(self, store_path: str, embeddings):
        self.store_path = store_path
        self.embeddings = embeddings

    def _load_articles(self):
        """Fetch articles from SQLite and convert to LangChain Documents."""
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

    def build(self):
        """Build FAISS index from DB articles."""
        docs = self._load_articles()
        if not docs:
            logging.warning("No articles found in database.")
            return None

        store = FAISS.from_documents(docs, self.embeddings)
        store.save_local(self.store_path)
        logging.info(f"FAISS index built and saved at {self.store_path}")
        return store

    def load(self):
        """Load FAISS index if available, else build it."""
        if os.path.exists(self.store_path):
            store = FAISS.load_local(
                self.store_path,
                self.embeddings,
                allow_dangerous_deserialization=True,
            )
            logging.info("Loaded existing FAISS index.")
            return store
        else:
            logging.warning("FAISS index not found. Building new one...")
            return self.build()

    def search(self, query: str, k: int = 5):
        """Perform semantic search on FAISS index."""
        store = self.load()
        if not store:
            logging.error("Cannot search, FAISS index unavailable.")
            return []
        return store.similarity_search(query, k=k)
