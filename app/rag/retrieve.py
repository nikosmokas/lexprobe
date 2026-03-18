from qdrant_client import QdrantClient
from .embed import embed

qdrant = QdrantClient(host="localhost", port=6333)

COLLECTION_NAME = "legal_chunks"

def retrieve(query: str, k: int = 5):
    results = qdrant.query_points(
        collection_name=COLLECTION_NAME,
        query=embed(query),
        limit=k
    )

    return [r.payload for r in results.points]