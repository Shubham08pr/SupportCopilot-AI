from backend.ingestion.vector_store import FAISSStore
from backend.app.services.embedding_service import get_embedding

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[3]
STORE_PATH = BASE_DIR / "faiss_store.pkl"



store = FAISSStore()
# store.load("backend/ingestion/faiss_store.pkl")
store.load(str(STORE_PATH))

def retrieve_chunks(query: str, k=3):
    from backend.ingestion.vector_store import FAISSStore
    from backend.app.services.embedding_service import get_embedding

    store = FAISSStore()
    store.load("faiss_store.pkl")

    query_vector = get_embedding(query)
    results = store.search(query_vector, k)

    # 🔥 FILTER (important)
    filtered = [r for r in results if r["score"] < 1.2]

    return filtered

def compute_retrieval_confidence(results):
    """
    Converts FAISS similarity score
    into retrieval confidence
    """

    if not results:
        return 0.0

    score = results[0]["score"]

    if score < 0.8:
        return 0.9
    elif score < 1.0:
        return 0.75
    elif score < 1.2:
        return 0.6
    else:
        return 0.3

def compute_confidence(retrieval_confidence, llm_confidence):
    """
    Hybrid confidence scoring
    """

    final_score = (
        0.7 * retrieval_confidence +
        0.3 * llm_confidence
    )

    return round(final_score, 2)