from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from scrap_api import scrape_articles

app = FastAPI(title="News Scraper API")

# ✅ Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # in production, replace "*" with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Welcome to the News Scraper API 🚀"}

@app.get("/scrape")
def scrape(limit: int = Query(10, description="Number of articles to fetch")):
    """
    Fetch latest news articles from Dawn.
    """
    articles = scrape_articles(limit=limit)
    return {
        "status": "success",
        "count": len(articles),
        "articles": articles
    }
