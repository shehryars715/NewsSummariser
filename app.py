import streamlit as st
import sqlite3
import os
from datetime import datetime, timedelta
import pandas as pd

# Import functions from existing modules
from db import init_db, article_exists, insert_article
from faiss_manager import FAISSManager
from summariser import summarize
from embed_and_search import load_faiss_index, search_faiss, summarize_articles
from config import DB_FILE, FAISS_STORE_PATH
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI

# Load CSS
def load_css():
    with open("styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Initialize components
@st.cache_resource
def init_components():
    """Initialize database and AI components"""
    init_db()
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.4)
    faiss_manager = FAISSManager(FAISS_STORE_PATH, embeddings)
    return embeddings, llm, faiss_manager

def get_articles_from_db(limit=20, category_filter=None, hours_filter=24):
    """Fetch articles from database with filters"""
    conn = sqlite3.connect(DB_FILE)
    query = """
        SELECT id, title, excerpt, publish_time, url, content, category, scraped_at 
        FROM articles 
        WHERE scraped_at >= datetime('now', '-{} hours')
    """.format(hours_filter)
    
    params = []
    if category_filter and category_filter != "All":
        query += " AND category = ?"
        params.append(category_filter)
    
    query += " ORDER BY scraped_at DESC LIMIT ?"
    params.append(limit)
    
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df

def get_categories():
    """Get unique categories from database"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT category FROM articles WHERE category IS NOT NULL")
    categories = [row[0] for row in cursor.fetchall()]
    conn.close()
    return ["All"] + categories

def get_article_stats():
    """Get basic statistics about articles"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Total articles
    cursor.execute("SELECT COUNT(*) FROM articles")
    total = cursor.fetchone()[0]
    
    # Articles in last 24 hours
    cursor.execute("SELECT COUNT(*) FROM articles WHERE scraped_at >= datetime('now', '-24 hours')")
    last_24h = cursor.fetchone()[0]
    
    conn.close()
    return total, last_24h

def main():
    # Load CSS
    if os.path.exists("styles.css"):
        load_css()
    
    # Initialize components
    embeddings, llm, faiss_manager = init_components()
    
    # App header
    st.markdown('<div class="header">', unsafe_allow_html=True)
    st.title("🗞️ Dawn News Intelligence")
    st.markdown("*AI-Powered News Aggregation & Search*")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.markdown('<div class="sidebar-header">Navigation</div>', unsafe_allow_html=True)
    
    # Navigation
    page = st.sidebar.selectbox(
        "Choose a page:",
        ["📰 Latest News", "🤖 AI Summary"]
    )
    
    # Get categories for filtering
    categories = get_categories()
    
    if page == "📰 Latest News":
        st.markdown('<div class="page-header">Latest News Articles</div>', unsafe_allow_html=True)
        
        # Filters
        col1, col2, col3 = st.columns(3)
        with col1:
            category_filter = st.selectbox("Category:", categories)
        with col2:
            hours_filter = st.selectbox("Time Range:", [6, 12, 24, 48], index=2)
        with col3:
            limit = st.selectbox("Number of Articles:", [10, 20, 50], index=1)
        
        # Fetch and display articles
        df = get_articles_from_db(limit, category_filter, hours_filter)
        
        if df.empty:
            st.warning("No articles found with the current filters.")
        else:
            st.success(f"Found {len(df)} articles")
            
            # Display articles
            for idx, row in df.iterrows():
                with st.container():
                    st.markdown(f'<div class="article-card">', unsafe_allow_html=True)
                    
                    # Article header
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(f'<h3 class="article-title">{row["title"]}</h3>', unsafe_allow_html=True)
                        st.markdown(f'<span class="article-category">{row["category"]}</span>', unsafe_allow_html=True)
                    with col2:
                        st.markdown(f'<div class="article-time">{row["scraped_at"]}</div>', unsafe_allow_html=True)
                    
                    # Article content
                    st.markdown(f'<p class="article-excerpt">{row["excerpt"]}</p>', unsafe_allow_html=True)
                    
                    # Article actions
                    col1, col2, col3 = st.columns([1, 1, 2])
                    with col1:
                        if st.button(f"Read Full", key=f"read_{idx}"):
                            st.markdown(f'<div class="article-content">{row["content"]}</div>', unsafe_allow_html=True)
                    with col2:
                        st.markdown(f'<a href="{row["url"]}" target="_blank" class="article-link">Original →</a>', unsafe_allow_html=True)
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                    st.markdown("---")
    
    elif page == "🤖 AI Summary":
        st.markdown('<div class="page-header">AI-Powered News Summary</div>', unsafe_allow_html=True)
        st.markdown("Get intelligent summaries of recent news")
        
        # Summary options
        col1, col2 = st.columns(2)
        with col1:
            summary_type = st.selectbox("Summary Type:", ["Recent News", "Custom Search"])
            hours_range = st.selectbox("Time Range:", [6, 12, 24, 48], index=2)
        with col2:
            category_filter = st.selectbox("Focus Category:", categories)
            max_articles = st.slider("Max Articles to Analyze:", 3, 20, 10)
        
        if summary_type == "Custom Search":
            search_query = st.text_input("Search Query for Summary:", placeholder="e.g., 'government policies', 'sports news'")
        
        if st.button("📝 Generate Summary", type="primary"):
            with st.spinner("Analyzing articles and generating summary..."):
                try:
                    if summary_type == "Recent News":
                        # Get recent articles
                        df = get_articles_from_db(max_articles, category_filter, hours_range)
                        if df.empty:
                            st.warning("No articles found for the selected criteria.")
                        else:
                            # Convert to document format for summarization
                            from langchain.schema import Document
                            documents = []
                            for _, row in df.iterrows():
                                doc_text = f"{row['title']}\n\n{row['excerpt']}\n\n{row['content']}"
                                documents.append(Document(
                                    page_content=doc_text,
                                    metadata={"url": row['url'], "category": row['category']}
                                ))
                            
                            # Generate summary
                            summary = summarize(documents, llm)
                            st.markdown(f'<div class="summary-box">{summary}</div>', unsafe_allow_html=True)
                    
                    else:  # Custom Search
                        if not search_query:
                            st.warning("Please enter a search query.")
                        else:
                            # Search and summarize
                            results = search_faiss(search_query, k=max_articles)
                            if results:
                                summary = summarize_articles(results)
                                st.markdown(f'<div class="summary-box">{summary}</div>', unsafe_allow_html=True)
                            else:
                                st.warning("No articles found for the search query.")
                                
                except Exception as e:
                    st.error(f"Summary generation failed: {str(e)}")
    
    # Footer
    st.markdown("---")
    st.markdown('<div class="footer">Built with Streamlit • Powered by Google Gemini AI</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()