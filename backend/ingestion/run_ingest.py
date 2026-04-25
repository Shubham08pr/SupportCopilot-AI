import os
from pathlib import Path

from backend.ingestion.embedder import embed_chunks
from backend.ingestion.loader import load_files
from backend.ingestion.builder import build_chunks
from backend.ingestion.vector_store import FAISSStore

# 🔥 Always resolve project root correctly
BASE_DIR = Path(__file__).resolve().parents[2]
DATA_PATH = BASE_DIR / "data"

def main():
    print("🔍 DATA PATH:", DATA_PATH)
    print("📂 EXISTS:", DATA_PATH.exists())

    if not DATA_PATH.exists():
        raise Exception("Data folder not found!")

    print("📥 Loading documents...")
    docs = load_files(str(DATA_PATH))

    print("✂️ Chunking...")
    chunks = build_chunks(docs)

    print("🧠 Generating embeddings...")
    embedded_chunks = embed_chunks(chunks)

    print("📦 Storing in FAISS...")
    store = FAISSStore()
    store.add(embedded_chunks)

    print("💾 Saving index...")
    store.save(str(STORE_PATH))

    print("📄 Total documents:", len(docs))
    print("✂️ Total chunks:", len(chunks))
    print("📊 Total embedded chunks:", len(embedded_chunks))

if __name__ == "__main__":
    main()