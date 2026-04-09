from fastapi import APIRouter, HTTPException

from src.app.schemas.models import QueryRequest, RAGResponse, ArticleSummary
from src.app.services.rag import retrieve_articles
from src.app.services.llm import generate_summary

router = APIRouter()


@router.post("/query", response_model=RAGResponse)
async def query_articles(request: QueryRequest):
    """Main RAG endpoint - retrieve articles and generate summary."""
    try:
        articles = retrieve_articles(request.query, request.max_articles)

        if not articles:
            raise HTTPException(status_code=404, detail="No relevant articles found")

        summary = generate_summary(request.query, articles)
        articles_used = [ArticleSummary(**article) for article in articles]

        return RAGResponse(
            query=request.query,
            summary=summary,
            articles_used=articles_used,
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")


@router.post("/search")
async def search_articles(request: QueryRequest):
    """Search for articles without generating summary."""
    try:
        articles = retrieve_articles(request.query, request.max_articles)
        return {
            "query": request.query,
            "articles": [ArticleSummary(**article) for article in articles],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching articles: {str(e)}")
