def compute_confidence(results):
    if not results:
        return 0.0

    scores = [r["score"] for r in results]

    # Qdrant cosine similarity is already 0–1-ish
    return round(sum(scores) / len(scores), 3)

def extract_sources(results):
    sources = []

    for r in results:
        sources.append({
            "doc_id": r["doc_id"],
            "article": r["article"]
        })

    return sources