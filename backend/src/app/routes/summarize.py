from fastapi import APIRouter, HTTPException

from src.app.schemas.models import URLSummaryRequest, URLSummaryResponse
from src.app.services.rag import get_article_by_url
from src.app.services.llm import generate_article_summary

router = APIRouter()


@router.post("/summarize-url", response_model=URLSummaryResponse)
async def summarize_by_url(request: URLSummaryRequest):
    """Summarize a specific article by URL."""
    article = get_article_by_url(request.url)

    if not article:
        raise HTTPException(status_code=404, detail="Article not found in database")

    if not article.get('content') or article['content'] == 'No content found.':
        raise HTTPException(status_code=400, detail="Article content is not available")

    try:
        summary = generate_article_summary(article)

        return URLSummaryResponse(
            url=article['url'],
            title=article['title'],
            summary=summary,
            category=article.get('category', 'Unknown'),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating summary: {str(e)}")
