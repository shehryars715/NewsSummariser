import streamlit as st
import sqlite3
from datetime import datetime
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import time
from styles import apply_custom_styles

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="News Digest Hub",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Apply custom styles
apply_custom_styles()

# Categories with icons
CATEGORIES = {
    "Technology and Innovation": "🚀",
    "Corporate and Business News": "💎", 
    "Sports and Athletics": "⚡",
    "National News from Pakistan": "🏛️",
    "Others": "✨"
}

# Category CSS classes
CATEGORY_CLASSES = {
    "Technology and Innovation": "category-tech",
    "Corporate and Business News": "category-business",
    "Sports and Athletics": "category-sports", 
    "National News from Pakistan": "category-national",
    "Others": "category-others"
}

@st.cache_data(ttl=300)
def connect_and_fetch_db():
    """Connect to database and fetch all articles"""
    try:
        conn = sqlite3.connect("data/articles.db")
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT title, excerpt, publish_time, url, category
            FROM articles
            ORDER BY publish_time DESC
        """)
        articles = cursor.fetchall()
        conn.close()
        
        return articles
    except sqlite3.Error as e:
        st.error(f"Database error: {e}")
        return []

def get_articles_by_category(articles):
    """Organize articles by category"""
    categorized = {cat: [] for cat in CATEGORIES.keys()}
    
    for article in articles:
        title, excerpt, publish_time, url, category = article
        if category in categorized:
            categorized[category].append({
                "title": title,
                "excerpt": excerpt,
                "publish_time": publish_time,
                "url": url
            })
    
    return categorized

@st.cache_resource
def init_gemini():
    """Initialize Gemini LLM"""
    try:
        return ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.5,
            max_output_tokens=800,
        )
    except Exception as e:
        st.error(f"Failed to initialize Gemini: {e}")
        return None

def summarize_category(llm, category, articles):
    """Generate AI summary for a category"""
    if not articles or not llm:
        return None
    
    template = """
    You are a professional news analyst. Create an insightful, engaging summary of these {category} articles.
    
    Focus on:
    - Key trends and emerging patterns
    - Most significant developments
    - Impact and implications
    - 3-5 concise bullet points
    - Professional, informative tone
    
    Articles:
    {articles}
    
    Provide a strategic overview highlighting the most important insights and trends.
    """
    
    prompt = PromptTemplate(
        input_variables=["category", "articles"],
        template=template
    )
    
    chain = prompt | llm | StrOutputParser()
    
    formatted_articles = "\n".join(
        f"• {a['title']} ({a['publish_time']}): {a['excerpt'][:150]}..."
        for a in articles[:6]
    )
    
    try:
        result = chain.invoke({"category": category, "articles": formatted_articles})
        return result
    except Exception as e:
        st.error(f"AI summarization failed: {e}")
        return None

def display_category_card(category, articles, icon, css_class):
    """Display a beautifully styled category card"""
    st.markdown(f"""
    <div class="category-card {css_class}" style="--category-gradient: var(--{css_class.split('-')[1]}-gradient);">
        <h2 class="category-title">
            <span class="category-icon">{icon}</span>
            {category}
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    if not articles:
        st.markdown("""
        <div class="no-articles">
            <h3>📭 No Recent Articles</h3>
            <p>Stay tuned for updates in this category!</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Show AI summary
    if st.session_state.get('show_summaries', True):
        with st.expander(f"🤖 AI Intelligence Summary - {category}", expanded=False):
            if f"summary_{category}" in st.session_state:
                st.markdown(f"**📊 Strategic Overview:**")
                st.write(st.session_state[f"summary_{category}"])
            else:
                st.info("🎯 Generate AI summaries to unlock strategic insights and trend analysis!")
    
    # Display articles with enhanced styling
    for i, article in enumerate(articles[:8]):
        st.markdown(f"""
        <div class="article-item">
            <div class="article-title">📰 {article['title']}</div>
            <div class="article-excerpt">{article['excerpt']}</div>
            <div class="article-meta">
                <span>🕒 {article['publish_time']}</span>
                <a href="{article['url']}" target="_blank" class="article-url">Read Full Story →</a>
            </div>
        </div>
        """, unsafe_allow_html=True)

def render_header():
    """Render the animated header"""
    st.markdown("""
    <div class="main-header">
        <h1 class="main-title">🌟 News Digest Hub</h1>
        <p class="main-subtitle">Experience news like never before • AI-powered insights • Real-time updates</p>
    </div>
    """, unsafe_allow_html=True)

def render_control_panel():
    """Render the control panel"""
    st.markdown('<div class="control-panel">', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
    
    with col1:
        refresh_clicked = st.button("🔄 Refresh Articles", type="primary")
    
    with col2:
        generate_summaries = st.button("🧠 Generate AI Insights", type="secondary")
    
    with col3:
        if st.button("📊 Analytics Mode", type="secondary"):
            st.info("Coming soon: Advanced analytics dashboard!")
    
    with col4:
        show_summaries = st.checkbox("AI Summaries", value=st.session_state.get('show_summaries', True))
        st.session_state.show_summaries = show_summaries
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    return refresh_clicked, generate_summaries

def render_statistics(total_articles, categories_with_articles):
    """Render the statistics cards"""
    latest_update = datetime.now().strftime('%H:%M:%S')
    
    st.markdown(f"""
    <div class="stats-container">
        <div class="stat-card">
            <div class="stat-number">{total_articles}</div>
            <div class="stat-label">📊 Total Articles</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">{categories_with_articles}</div>
            <div class="stat-label">🗂️ Active Categories</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">{latest_update}</div>
            <div class="stat-label">⏰ Last Refresh</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">AI</div>
            <div class="stat-label">🤖 Powered Analysis</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def generate_ai_summaries(categorized_articles):
    """Generate AI summaries for all categories"""
    llm = init_gemini()
    if not llm:
        st.error("Failed to initialize AI model")
        return False
    
    with st.spinner("🧠 Generating AI insights and trend analysis..."):
        progress_bar = st.progress(0)
        summary_status = st.empty()
        
        for i, (category, articles) in enumerate(categorized_articles.items()):
            if articles:
                summary_status.info(f"🔍 Analyzing {category}...")
                summary = summarize_category(llm, category, articles)
                if summary:
                    st.session_state[f"summary_{category}"] = summary
            progress_bar.progress((i + 1) / len(categorized_articles))
        
        summary_status.empty()
        progress_bar.empty()
        
        st.markdown("""
        <div class="success-message">
            <h4>✅ AI Analysis Complete!</h4>
            <p>Strategic insights and trend analysis are now available for all categories.</p>
        </div>
        """, unsafe_allow_html=True)
        time.sleep(2)
        
    return True

def render_footer():
    """Render the footer"""
    st.markdown("""
    <div class="main-header" style="margin-top: 4rem; padding: 2rem;">
        <h3 style="color: rgba(255,255,255,0.9); margin: 0;">🚀 Powered by Advanced AI Technology</h3>
        <p style="color: rgba(255,255,255,0.7); margin: 0.5rem 0 0 0;">
            Real-time updates • Intelligent categorization • Strategic insights
        </p>
    </div>
    """, unsafe_allow_html=True)

def main():
    """Main application function"""
    # Render header
    render_header()
    
    # Render control panel
    refresh_clicked, generate_summaries = render_control_panel()
    
    # Handle refresh
    if refresh_clicked:
        st.cache_data.clear()
        st.rerun()
    
    # Load articles
    with st.spinner("🚀 Loading latest articles..."):
        articles = connect_and_fetch_db()
    
    if not articles:
        st.markdown("""
        <div class="error-container">
            <h3>⚠️ Connection Issue</h3>
            <p>Unable to load articles. Please check database connection.</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Organize articles
    categorized_articles = get_articles_by_category(articles)
    
    # Render statistics
    total_articles = len(articles)
    categories_with_articles = sum(1 for cat_articles in categorized_articles.values() if cat_articles)
    render_statistics(total_articles, categories_with_articles)
    
    # Handle AI summary generation
    if generate_summaries:
        if generate_ai_summaries(categorized_articles):
            st.rerun()
    
    # Display categories
    st.markdown("## 🗞️ News Categories • Live Updates")
    
    for category, articles in categorized_articles.items():
        icon = CATEGORIES[category]
        css_class = CATEGORY_CLASSES[category]
        display_category_card(category, articles, icon, css_class)
        st.markdown("<br>", unsafe_allow_html=True)
    
    # Render footer
    render_footer()

if __name__ == "__main__":
    main()