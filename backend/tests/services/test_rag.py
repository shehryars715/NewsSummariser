import pytest

from src.app.services import rag


def test_retrieve_articles_requires_loaded_index(monkeypatch):
    monkeypatch.setattr(rag, "faiss_index", None)
    monkeypatch.setattr(rag, "metadata", None)

    with pytest.raises(rag.HTTPException) as exc_info:
        rag.retrieve_articles("stock")

    assert exc_info.value.status_code == 500
    assert exc_info.value.detail == "FAISS index not loaded"


def test_retrieve_articles_returns_ranked_articles(monkeypatch):
    class FakeEmbeddingModel:
        def embed_query(self, query):
            assert query == "stock market"
            return [0.1, 0.2, 0.3]

    class FakeIndex:
        def search(self, query_vector, k):
            assert k == 2
            return [[0.25, 1.0]], [[1, 0]]

    monkeypatch.setattr(rag, "faiss_index", FakeIndex())
    monkeypatch.setattr(
        rag,
        "metadata",
        [
            {
                "title": "Oil prices steady",
                "excerpt": "Energy shares were mixed.",
                "url": "https://example.com/1",
                "category": "Corporate and Business News",
            },
            {
                "title": "Stocks rise after earnings beat",
                "excerpt": "Markets closed higher on Thursday.",
                "url": "https://example.com/2",
                "category": "Corporate and Business News",
            },
        ],
    )
    monkeypatch.setattr(rag, "get_embedding_model", lambda: FakeEmbeddingModel())

    articles = rag.retrieve_articles("stock market", k=2)

    assert [article["title"] for article in articles] == [
        "Stocks rise after earnings beat",
        "Oil prices steady",
    ]
    assert articles[0]["relevance_score"] == pytest.approx(1 / 1.25)
    assert articles[1]["relevance_score"] == pytest.approx(0.5)
