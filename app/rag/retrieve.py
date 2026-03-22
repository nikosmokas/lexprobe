from qdrant_client import QdrantClient
from .embed import embed

qdrant = QdrantClient(host="localhost", port=6333)

COLLECTION_NAME = "legal_chunks"

from .rerank import rerank


def dedupe(results):
    seen = set()
    unique = []

    for r in results:
        key = r.get("text", "")[:100]
        if key not in seen:
            seen.add(key)
            unique.append(r)

    return unique


def retrieve(query: str, k: int = 10):
    results = qdrant.query_points(
        collection_name=COLLECTION_NAME,
        query=embed(query),
        limit=k
    )

    enriched = []
    for r in results.points:
        payload = r.payload
        payload["score"] = r.score
        enriched.append(payload)

    # 🔥 apply reranking
    final_results = rerank(query, enriched, top_k=3)

    # dedupe similar chunks and enforce hard 3 chunk limit
    final_results = dedupe(final_results)
    final_results = final_results[:3]

    return final_results