import sqlite3
import os
from dotenv import load_dotenv

from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain.prompts import ChatPromptTemplate
from langchain.schema import Document
from config import DB_FILE

# Load environment variables
load_dotenv()

# ✅ Initialize Gemini
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.4)

FAISS_STORE_PATH = "faiss_store"


def load_articles_from_db():
    """Load all articles from SQLite and convert to LangChain Documents."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, excerpt, content, url, category FROM articles")
    rows = cursor.fetchall()
    conn.close()

    documents = []
    for r in rows:
        doc_text = f"{r[1]}\n\n{r[2]}\n\n{r[3]}"
        documents.append(
            Document(
                page_content=doc_text,
                metadata={"id": r[0], "url": r[4], "category": r[5]},
            )
        )
    return documents


def build_faiss_index():
    """Build FAISS index from SQLite articles."""
    documents = load_articles_from_db()
    if not documents:
        print("⚠️ No articles found in database.")
        return None

    vectorstore = FAISS.from_documents(documents, embeddings)
    vectorstore.save_local(FAISS_STORE_PATH)
    print(f"✅ FAISS index built and saved at {FAISS_STORE_PATH}")
    return vectorstore


def load_faiss_index():
    """Load FAISS index if it exists, else build it."""
    if os.path.exists(FAISS_STORE_PATH):
        vectorstore = FAISS.load_local(
            FAISS_STORE_PATH,
            embeddings,
            allow_dangerous_deserialization=True,
        )
        print("📂 Loaded existing FAISS index.")
        return vectorstore
    else:
        print("⚠️ FAISS index not found. Building new one...")
        return build_faiss_index()


def search_faiss(query, k=5):
    """Search FAISS index with a query string."""
    vectorstore = load_faiss_index()
    if vectorstore is None:
        print("⚠️ Cannot search, FAISS index not available.")
        return []

    results = vectorstore.similarity_search(query, k=k)
    return results


def summarize_articles(articles):
    """Summarize retrieved articles using Gemini + PromptTemplate (latest LangChain style)."""
    combined_text = "\n\n".join([a.page_content for a in articles])

    prompt = ChatPromptTemplate.from_template(
        """
        You are a helpful assistant. Summarize the following news articles into a concise report. 
        - Highlight the main events.
        - Group similar points together.
        - Keep the summary factual and objective.
        - Limit to about 200 words.
        - Also cite the URL links for reference.

        Articles:
        {articles}

        Summary:
        """
    )

    # ✅ New runnable chain style
    chain = prompt | llm
    summary = chain.invoke({"articles": combined_text})
    return summary.content  # .content holds the text from ChatGoogleGenerativeAI


if __name__ == "__main__":
    # Example: build index
    #build_faiss_index()

    # Example: query
    query = "Flood news"
    results = search_faiss(query, k=3)

    # 🔹 Summarize
    if results:
        print("\n📝 Gemini Summary:")
        summary = summarize_articles(results)
        print(summary)
