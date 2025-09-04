import faiss
import numpy as np
import pickle
from config import embedding_model

def search_articles(query, k=5):
    """Search for similar articles using FAISS."""
    try:
        # Load index and metadata
        index = faiss.read_index("faiss_index.bin")
        with open("metadata.pkl", 'rb') as f:
            metadata = pickle.load(f)
        
        # Generate query embedding
        query_embedding = embedding_model.embed_query(query)
        query_vector = np.array([query_embedding], dtype=np.float32)
        
        # Search
        distances, indices = index.search(query_vector, k)
        
        # Show results
        print(f"\nSearch results for: '{query}'")
        print("-" * 50)
        
        for i, (distance, idx) in enumerate(zip(distances[0], indices[0])):
            article = metadata[idx]
            score = 1 / (1 + distance)
            
            print(f"{i+1}. {article['title']}")
            print(f"   Score: {score:.3f}")
            print(f"   Category: {article['category']}")
            print(f"   {article['excerpt'][:150]}...")
            print()
    
    except FileNotFoundError:
        print("FAISS index not found. Run the embedding generator first.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    while True:
        query = input("Search query (or 'quit'): ")
        if query.lower() == 'quit':
            break
        search_articles(query)