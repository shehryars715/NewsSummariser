const API_BASE_URL = 'https://newssummariser-5a49.onrender.com';

export interface Article {
  id?: number;
  title: string;
  excerpt?: string;
  url: string;
  category?: string;
  relevance_score?: number;
  publish_time?: string;
  content?: string;
}

export interface SearchResponse {
  articles: Article[];
}

export interface QueryResponse {
  summary: string;
  articles_used: Article[];
}

export interface SummarizeResponse {
  title: string;
  summary: string;
  category?: string;
  url: string;
}

export async function searchArticles(query: string, maxArticles: number = 5): Promise<SearchResponse> {
  const response = await fetch(`${API_BASE_URL}/search`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      query,
      max_articles: maxArticles,
    }),
  });

  if (!response.ok) {
    throw new Error(`Search failed: ${response.statusText}`);
  }

  return response.json();
}

export async function queryWithAISummary(query: string, maxArticles: number = 3): Promise<QueryResponse> {
  const response = await fetch(`${API_BASE_URL}/query`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      query,
      max_articles: maxArticles,
    }),
  });

  if (!response.ok) {
    throw new Error(`Query failed: ${response.statusText}`);
  }

  return response.json();
}

export async function summarizeArticleByUrl(url: string): Promise<SummarizeResponse> {
  const response = await fetch(`${API_BASE_URL}/summarize-url`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      url,
    }),
  });

  if (!response.ok) {
    throw new Error(`Summarization failed: ${response.statusText}`);
  }

  return response.json();
}