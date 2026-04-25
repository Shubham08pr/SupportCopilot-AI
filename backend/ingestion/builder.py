from backend.ingestion.chunker import chunk_text

def build_chunks(documents):
    chunked_docs = []

    for doc in documents:
        chunks = chunk_text(doc["text"])

        for chunk in chunks:
            chunked_docs.append({
                "text": chunk,
                "metadata": {
                    "category": doc["category"],
                    "file_name": doc["file_name"],
                    "source_path": doc["path"]
                }
            })

    return chunked_docs