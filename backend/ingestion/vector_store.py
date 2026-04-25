import faiss
import numpy as np
import pickle

class FAISSStore:
    def __init__(self, dim=1536):
        self.index = faiss.IndexFlatL2(dim)
        self.metadata = []

    def add(self, embedded_docs):
        vectors = []

        for doc in embedded_docs:
            vectors.append(doc["vector"])
            self.metadata.append({
                "text": doc["text"],
                "metadata": doc["metadata"]
            })

        vectors = np.array(vectors).astype("float32")
        self.index.add(vectors)

    def save(self, path="faiss_store.pkl"):
        with open(path, "wb") as f:
            pickle.dump((self.index, self.metadata), f)

    def load(self, path="faiss_store.pkl"):
        with open(path, "rb") as f:
            self.index, self.metadata = pickle.load(f)

    def search(self, query_vector, k=3):
        query_vector = np.array([query_vector]).astype("float32")

        distances, indices = self.index.search(query_vector, k)

        results = []
        for i in indices[0]:
            results.append(self.metadata[i])

        return results