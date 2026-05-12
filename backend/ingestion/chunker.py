def chunk_text(text, category, chunk_size=500, overlap=50):
    chunks = []

    # 🔥 1. FAQ → split by Q&A (BEST QUALITY)
    if category == "faq":
        parts = text.split("Q:")

        for part in parts:
            part = part.strip()
            if not part:
                continue

            chunk = "Q: " + part
            chunks.append(chunk)

        return chunks

    # 🔥 2. Tickets → keep as-is (already small)
    elif category == "tickets":
        return [text.strip()]

    # 🔥 3. Fallback → sliding window (your original logic)
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap

    return chunks