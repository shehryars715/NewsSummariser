# News RAG Backend

A Python backend that scrapes news articles from Geo.tv, stores them in Supabase, generates semantic embeddings locally using `BAAI/bge-base-en-v1.5`, and exposes a RAG (Retrieval-Augmented Generation) API that returns AI-generated summaries via Google Gemini.

## Features

- **Automated News Scraping** — Scrapes latest articles from Geo.tv on a 2-hour loop
- **Article Categorization** — Classifies articles using Hugging Face BART zero-shot classification
- **Local Semantic Search** — FAISS index built from local BGE embeddings (no external embedding API)
- **RAG API** — FastAPI server that retrieves relevant articles and generates summaries with Gemini
- **Cloud Storage** — Supabase for article storage and FAISS index persistence
- **Auto Cleanup** — Removes articles older than 1 day each cycle

## Architecture

```
┌──────────────┐     ┌────────────────┐     ┌──────────────┐
│   Geo.tv     │────▶│  Scraper       │────▶│  Supabase DB │
│  (News Src)  │     │  (scraper.py)  │     │  (Articles)  │
└──────────────┘     └────────────────┘     └──────────────┘
                            │                       │
                            ▼                       ▼
                     ┌────────────────┐     ┌──────────────────┐
                     │  Classifier    │     │  Local BGE Model │
                     │  (HF BART)    │     │  (bge-base-en)   │
                     └────────────────┘     └──────────────────┘
                                                    │
                                                    ▼
                                            ┌──────────────────┐
                                            │  FAISS Index     │
                                            │  (Supabase Stor) │
                                            └──────────────────┘
                                                    │
                                                    ▼
                                            ┌──────────────────┐
                                            │  FastAPI Server  │
                                            │  + Gemini LLM    │
                                            └──────────────────┘
```

## Prerequisites

- Python 3.10+
- Supabase account (database + storage bucket)
- Google Gemini API key (for summarization only)
- Hugging Face API token (for article categorization)

## Installation

```bash
git clone https://github.com/shehryars715/NewsSummariser/
cd NewsSummariser/backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the `backend/` directory:

```env
# Supabase
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key

# Google Gemini (used for summarization)
GEMINI_API_KEY=your_gemini_api_key

# Hugging Face (used for article categorization)
HF_TOKEN=your_hugging_face_token

# Optional: override the default embedding model
# EMBEDDING_MODEL=BAAI/bge-base-en-v1.5
```

## Database Setup

### Supabase Table

```sql
CREATE TABLE news_articles (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    excerpt TEXT,
    content TEXT,
    url TEXT UNIQUE NOT NULL,
    category TEXT,
    publish_time TIMESTAMPTZ,
    scraped_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_news_articles_url ON news_articles(url);
CREATE INDEX idx_news_articles_scraped_at ON news_articles(scraped_at);
CREATE INDEX idx_news_articles_category ON news_articles(category);
```

### Storage Bucket

Create a storage bucket named `Faiss` in Supabase for storing the FAISS index and metadata files.

## Usage

### Run the continuous scraper

Scrapes articles, classifies them, stores to DB, rebuilds embeddings, and cleans old articles — every 2 hours:

```bash
python main.py
```

### Start the API server

```bash
python -m src.app.main
# or
uvicorn src.app.main:app --host 0.0.0.0 --port 8000 --reload
```

## API Endpoints

### `GET /` — Health check

```json
{ "message": "News RAG API is running", "status": "healthy" }
```

### `POST /query` — RAG query (retrieve + summarize)

```json
{
  "query": "What's happening in Pakistan politics?",
  "max_articles": 3
}
```

**Response:**

```json
{
  "query": "What's happening in Pakistan politics?",
  "summary": "AI-generated summary...",
  "articles_used": [
    {
      "title": "Article Title",
      "excerpt": "Article excerpt...",
      "url": "https://www.geo.tv/latest/...",
      "category": "National News from Pakistan",
      "relevance_score": 0.85
    }
  ]
}
```

### `POST /search` — Semantic search only (no summary)

```json
{
  "query": "technology news",
  "max_articles": 5
}
```

### `POST /summarize-url` — Summarize a specific article by URL

```json
{
  "url": "https://www.geo.tv/latest/659168-..."
}
```

## Project Structure

```
backend/
├── main.py                          # Continuous scraping orchestrator
├── requirements.txt
├── .env
└── src/
    ├── core/
    │   ├── config.py                # Model config, lazy BGE loader
    │   └── database.py              # Supabase client
    ├── app/
    │   ├── main.py                  # FastAPI app entry point
    │   ├── routes/
    │   │   ├── query.py             # /query and /search endpoints
    │   │   └── summarize.py         # /summarize-url endpoint
    │   ├── schemas/
    │   │   └── models.py            # Pydantic request/response models
    │   └── services/
    │       ├── faiss_store.py       # FAISS index build + upload
    │       ├── rag.py               # FAISS search + article retrieval
    │       └── llm.py               # Gemini summarization
    ├── scraper/
    │   ├── scraper.py               # Scrape loop, DB insert, cleanup
    │   ├── parser.py                # HTML parsing, content extraction
    │   └── classifier.py            # HF BART zero-shot classification
    └── utils/
        └── helpers.py               # Embedding helper, human delay
```

## AI Models

| Purpose | Model | Runs |
|---|---|---|
| Embeddings | `BAAI/bge-base-en-v1.5` (768-dim) | Locally via Sentence Transformers |
| Summarization | `gemini-2.5-flash` | Remote via Google API |
| Classification | `facebook/bart-large-mnli` | Remote via Hugging Face Inference API |

The embedding model is downloaded from Hugging Face on first use and cached locally. No API key is needed for embeddings. The FAISS index dimension is derived automatically from the model.

## Scraping Settings

| Setting | Value |
|---|---|
| Source | `https://www.geo.tv/latest-news` |
| Interval | Every 2 hours (7200s) |
| Retention | Articles older than 1 day are deleted |
| Rate limiting | 2–4 second random delay between requests |

## Article Categories

- Technology and Innovation
- Corporate and Business News
- Sports and Athletics
- National News from Pakistan

## Troubleshooting

| Problem | Fix |
|---|---|
| FAISS index not loading | Check `Faiss` bucket exists in Supabase storage; re-run `faiss_create()` |
| Scraping returns nothing | Verify internet connection and that Geo.tv is accessible |
| Embedding model slow on first run | Normal — BGE weights (~440 MB) are downloaded once then cached |
| API 500 errors | Ensure `.env` variables are set and Supabase is reachable |

## License

MIT

For issues and questions:
1. Check the troubleshooting section
2. Review Supabase and API documentation
3. Create an issue in the repository
