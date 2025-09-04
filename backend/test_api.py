import requests
import json

# API base URL
BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint."""
    response = requests.get(f"{BASE_URL}/")
    print("Health Check:", response.json())

def test_stats():
    """Test stats endpoint."""
    response = requests.get(f"{BASE_URL}/stats")
    print("\nStats:", json.dumps(response.json(), indent=2))

def test_search(query):
    """Test search endpoint."""
    data = {"query": query, "max_articles": 3}
    response = requests.post(f"{BASE_URL}/search", json=data)
    
    if response.status_code == 200:
        result = response.json()
        print(f"\nSearch Results for: '{query}'")
        print("-" * 50)
        for i, article in enumerate(result["articles"], 1):
            print(f"{i}. {article['title']}")
            print(f"   Score: {article['relevance_score']:.3f}")
            print(f"   Category: {article['category']}")
            print(f"   URL: {article['url']}")
            print()
    else:
        print(f"Search failed: {response.status_code}, {response.text}")

def test_rag(query):
    """Test RAG endpoint."""
    data = {"query": query, "max_articles": 3}
    response = requests.post(f"{BASE_URL}/query", json=data)
    
    if response.status_code == 200:
        result = response.json()
        print(f"\nRAG Response for: '{query}'")
        print("=" * 60)
        print("SUMMARY:")
        print(result["summary"])
        print("\nSOURCE ARTICLES:")
        for i, article in enumerate(result["articles_used"], 1):
            print(f"{i}. {article['title']} (Score: {article['relevance_score']:.3f})")
        print("=" * 60)
    else:
        print(f"RAG query failed: {response.status_code}, {response.text}")

if __name__ == "__main__":
    print("Testing News RAG API")
    print("=" * 30)
    
    # Test endpoints
    test_health()
    test_stats()
    
    # Test queries
    queries = [
        "Pakistan cricket team performance",
        "technology trends in Pakistan",
        "business news today"
    ]
    
    for query in queries:
        test_search(query)
        test_rag(query)
        print("\n" + "="*80 + "\n")