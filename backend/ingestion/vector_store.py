import faiss
import numpy as np
import pickle


class FAISSStore:
    def __init__(self, dim=1536):
        self.index = faiss.IndexFlatL2(dim)
        self.texts = []        # ✅ store actual chunks
        self.metadata = []     # ✅ store metadata separately

    def add(self, embedded_docs):
        vectors = []

        for doc in embedded_docs:
            vectors.append(doc["vector"])

            # ✅ store cleanly
            self.texts.append(doc["text"])
            self.metadata.append(doc["metadata"])

        vectors = np.array(vectors).astype("float32")
        self.index.add(vectors)

    def save(self, path="faiss_store.pkl"):
        with open(path, "wb") as f:
            pickle.dump({
                "index": self.index,
                "texts": self.texts,
                "metadata": self.metadata
            }, f)

    def load(self, path="faiss_store.pkl"):
        with open(path, "rb") as f:
            data = pickle.load(f)

        self.index = data["index"]
        self.texts = data["texts"]
        self.metadata = data["metadata"]

    def search(self, query_vector, k=3):
        query_vector = np.array([query_vector]).astype("float32")

        distances, indices = self.index.search(query_vector, k)

        results = []

        for i, idx in enumerate(indices[0]):
            if idx == -1:
                continue

            results.append({
                "text": self.texts[idx],          # ✅ clean text
                "metadata": self.metadata[idx],   # ✅ clean metadata
                "score": float(distances[0][i])   # ✅ for confidence
            })

        # optional but good
        results.sort(key=lambda x: x["score"])

        return results