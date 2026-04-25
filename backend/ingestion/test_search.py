from vector_store import FAISSStore
from app.services.embedding_service import get_embedding

store = FAISSStore()
store.load("faiss_store.pkl")

query = "refund issue"

query_vector = get_embedding(query)

results = store.search(query_vector)

for r in results:
    print("\n---")
    print(r["metadata"])
    print(r["text"])