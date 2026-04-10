from src.app.services import llm


class FakeResponse:
    def __init__(self, content):
        self.content = content


class FakeLLM:
    def __init__(self):
        self.calls = []
        self.invocations = []

    def __call__(self, messages):
        self.calls.append(messages)
        return FakeResponse("article summary")

    def invoke(self, messages):
        self.invocations.append(messages)
        return FakeResponse("query summary")


def test_generate_article_summary_builds_prompt_from_article(monkeypatch):
    fake_llm = FakeLLM()
    monkeypatch.setattr(llm, "llm", fake_llm)

    article = {
        "title": "Market Wrap",
        "excerpt": "Stocks climbed into the close.",
        "content": "A broad rally pushed major indexes higher.",
    }

    summary = llm.generate_article_summary(article)

    assert summary == "article summary"
    prompt_text = "\n".join(str(message) for message in fake_llm.calls[0])
    assert "Market Wrap" in prompt_text
    assert "A broad rally pushed major indexes higher." in prompt_text


def test_generate_summary_includes_query_and_articles(monkeypatch):
    fake_llm = FakeLLM()
    monkeypatch.setattr(llm, "llm", fake_llm)

    articles = [
        {"title": "Stocks edge higher", "excerpt": "Investors reacted to new inflation data."},
        {"title": "Oil slips", "excerpt": "Energy markets softened on Friday."},
    ]

    summary = llm.generate_summary("stock market today", articles)

    assert summary == "query summary"
    prompt_text = "\n".join(str(message) for message in fake_llm.invocations[0])
    assert "stock market today" in prompt_text
    assert "Stocks edge higher" in prompt_text
    assert "Oil slips" in prompt_text