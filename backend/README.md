# News RAG Backend

A Python backend system that scrapes news articles from Dawn.com, stores them in Supabase, generates embeddings using Google's Gemini AI, and provides a RAG (Retrieval-Augmented Generation) API for intelligent news querying.

## 🚀 Features

- **Automated News Scraping**: Continuously scrapes latest news from Dawn.com every 2 hours
- **Intelligent Categorization**: Uses Hugging Face BART model to classify articles into categories
- **Vector Search**: FAISS-based semantic search with Gemini embeddings
- **RAG API**: FastAPI endpoints for querying news with AI-generated summaries
- **Cloud Storage**: Supabase database and storage integration
- **Automatic Cleanup**: Removes articles older than 1 day

## 📋 System Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Dawn.com      │───▶│  Scraper Module  │───▶│   Supabase DB   │
│   (News Source) │    │  (scrape.py)     │    │   (Articles)    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │                        │
                                ▼                        ▼
                       ┌──────────────────┐    ┌─────────────────┐
                       │ Category Classifier│    │ FAISS Embeddings│
                       │ (Hugging Face)     │    │ (Gemini AI)     │
                       └──────────────────┘    └─────────────────┘
                                                        │
                                                        ▼
                                               ┌─────────────────┐
                                               │   RAG API       │
                                               │  (FastAPI)      │
                                               └─────────────────┘
```

## 🛠️ Prerequisites

- Python 3.8+
- Supabase account with database and storage bucket
- Google Gemini API key
- Hugging Face API token

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/shehryars715/NewsSummariser/
   cd backend
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Create environment file**
   ```bash
   cp .env.example .env
   ```

4. **Configure environment variables**
   ```env
   # Supabase Configuration
   SUPABASE_URL=your_supabase_project_url
   SUPABASE_KEY=your_supabase_anon_key

   # Google Gemini AI
   GEMINI_API_KEY=your_gemini_api_key

   # Hugging Face (for article categorization)
   HF_TOKEN=your_hugging_face_token
   ```

## 🗄️ Database Setup

### Supabase Table Schema

Create a table named `news_articles` with the following structure:

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

-- Add indexes for better performance
CREATE INDEX idx_news_articles_url ON news_articles(url);
CREATE INDEX idx_news_articles_scraped_at ON news_articles(scraped_at);
CREATE INDEX idx_news_articles_category ON news_articles(category);
```

### Storage Bucket

Create a storage bucket named `Faiss` in your Supabase project for storing FAISS index files.

## 🚀 Usage

### 1. Run Continuous Scraper

Starts the main scraping loop that runs every 2 hours:

```bash
python main.py
```

**What it does:**
- Scrapes latest articles from Dawn.com
- Classifies articles into categories
- Stores in Supabase database
- Generates and updates FAISS embeddings
- Deletes articles older than 1 day

### 2. Run One-time Scrape

For manual scraping:

```bash
python scrape.py
```

### 3. Generate FAISS Index

To manually update the vector embeddings:

```bash
python faiss_store.py
```

### 4. Start RAG API Server

Launch the FastAPI server:

```bash
python rag_api.py
```

Or with uvicorn:
```bash
uvicorn rag_api:app --host 0.0.0.0 --port 8000 --reload
```

## 🔌 API Endpoints

### Base URL: `http://localhost:8000`

### 1. Health Check
```http
GET /
```
**Response:**
```json
{
    "message": "News RAG API is running",
    "status": "healthy"
}
```

### 2. Query Articles (RAG)
```http
POST /query
Content-Type: application/json

{
    "query": "What's happening in Pakistan politics?",
    "max_articles": 3
}
```

**Response:**
```json
{
    "query": "What's happening in Pakistan politics?",
    "summary": "AI-generated summary based on retrieved articles...",
    "articles_used": [
        {
            "title": "Article Title",
            "excerpt": "Article excerpt...",
            "url": "https://www.dawn.com/news/...",
            "category": "National News from Pakistan",
            "relevance_score": 0.85
        }
    ]
}
```

### 3. Search Articles Only
```http
POST /search
Content-Type: application/json

{
    "query": "technology news",
    "max_articles": 5
}
```

### 4. Summarize Specific Article
```http
POST /summarize-url
Content-Type: application/json

{
    "url": "https://www.dawn.com/news/1939445/..."
}
```

## 📁 File Structure

```
backend/
├── main.py              # Main scraping orchestrator
├── scrape.py            # Core scraping functionality
├── utils.py             # Helper functions (categorization, content extraction)
├── faiss_store.py       # FAISS index management
├── rag_api.py          # FastAPI RAG server
├── config.py           # Configuration and model initialization
├── test.py             # Testing utilities
├── .env                # Environment variables
├── .gitignore          # Git ignore file
└── requirements.txt    # Python dependencies
```

## ⚙️ Configuration

### Article Categories

The system classifies articles into these categories:
- Technology and Innovation
- Corporate and Business News
- Sports and Athletics
- National News from Pakistan

### Scraping Settings

- **Source**: Dawn.com latest news
- **Interval**: Every 2 hours (7200 seconds)
- **Retention**: Articles older than 1 day are automatically deleted
- **Rate Limiting**: 2-4 second delays between requests

### AI Models

- **Embeddings**: `models/embedding-001` (Google Gemini)
- **Chat**: `gemini-2.5-flash` (Google Gemini)
- **Classification**: `facebook/bart-large-mnli` (Hugging Face)

## 🔍 Monitoring

The system provides console output with Rich formatting:
- ✅ Successful operations
- ❌ Error indicators  
- ⚠️ Warnings
- 📊 Statistics and progress

## 🐛 Troubleshooting

### Common Issues

1. **FAISS Index Not Loading**
   - Check Supabase storage bucket exists
   - Verify storage permissions
   - Run `python faiss_store.py` to regenerate

2. **Scraping Failures**
   - Check internet connection
   - Verify Dawn.com is accessible
   - Review rate limiting delays

3. **API Errors**
   - Ensure all environment variables are set
   - Check Gemini API quota
   - Verify Supabase connection

### Debug Mode

Add debug logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```


## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section
2. Review Supabase and API documentation
3. Create an issue in the repository
