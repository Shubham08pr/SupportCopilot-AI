from ..app.services.embedding_service import get_embedding

def embed_chunks(chunks):
    embedded_docs = []

    for chunk in chunks:
        vector = get_embedding(chunk["text"])

        embedded_docs.append({
            "vector": vector,
            "text": chunk["text"],
            "metadata": chunk["metadata"]
        })

    return embedded_docs