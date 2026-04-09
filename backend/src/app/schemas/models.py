from pydantic import BaseModel
from typing import List


class QueryRequest(BaseModel):
    query: str
    max_articles: int = 3


class ArticleSummary(BaseModel):
    title: str
    excerpt: str
    url: str
    category: str
    relevance_score: float


class RAGResponse(BaseModel):
    query: str
    summary: str
    articles_used: List[ArticleSummary]


class URLSummaryRequest(BaseModel):
    url: str


class URLSummaryResponse(BaseModel):
    url: str
    title: str
    summary: str
    category: str
