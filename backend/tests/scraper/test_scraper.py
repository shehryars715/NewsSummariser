from bs4 import BeautifulSoup

from src.scraper import scraper


def test_get_latest_article_links_filters_duplicates_and_invalid_urls():
    html = """
    <div>
        <div>
            <a href="/latest/111-first-story">First Story</a>
            <span class="date">Apr 10, 2026</span>
        </div>
        <div>
            <a href="/latest/111-first-story">First Story Duplicate</a>
            <span class="date">Apr 10, 2026</span>
        </div>
        <div>
            <a href="/news/222-not-latest">Ignore Me</a>
            <span class="date">Apr 10, 2026</span>
        </div>
        <div>
            <a href="https://example.com/offsite">Offsite Story</a>
            <span class="date">Apr 10, 2026</span>
        </div>
    </div>
    """

    soup = BeautifulSoup(html, "html.parser")

    articles = scraper.get_latest_article_links(soup)

    assert len(articles) == 1
    assert articles[0]["title"] == "First Story"
    assert articles[0]["url"] == "https://www.geo.tv/latest/111-first-story"


def test_scrape_once_enriches_and_inserts_new_article(monkeypatch):
    inserted_articles = []

    class FakeRobotParser:
        def can_fetch(self, user_agent, url):
            return True

    monkeypatch.setattr(scraper, "check_supabase_connection", lambda: True)
    monkeypatch.setattr(scraper, "get_robot_parser", lambda: FakeRobotParser())
    monkeypatch.setattr(scraper, "get_latest_news_page", lambda: object())
    monkeypatch.setattr(
        scraper,
        "get_latest_article_links",
        lambda soup: [
            {
                "title": "Market rallies on investor optimism",
                "excerpt": "N/A",
                "publish_time": "N/A",
                "url": "https://www.geo.tv/latest/999-market-rally",
            }
        ],
    )
    monkeypatch.setattr(scraper, "article_exists", lambda url: False)
    monkeypatch.setattr(
        scraper,
        "scrape_article_content",
        lambda url: {
            "content": "Stocks moved higher after the central bank announcement.",
            "excerpt": "Equities gained during afternoon trading.",
            "publish_time": "Apr 10, 2026",
        },
    )
    monkeypatch.setattr(scraper, "classify_category", lambda text: "Corporate and Business News")
    monkeypatch.setattr(scraper, "human_delay", lambda: None)
    monkeypatch.setattr(scraper, "insert_article", inserted_articles.append)

    scraper.scrape_once()

    assert len(inserted_articles) == 1
    inserted = inserted_articles[0]
    assert inserted["excerpt"] == "Equities gained during afternoon trading."
    assert inserted["publish_time"] == "Apr 10, 2026"
    assert inserted["category"] == "Corporate and Business News"
    assert inserted["content"].startswith("Stocks moved higher")
