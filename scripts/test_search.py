from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient

model = SentenceTransformer("all-MiniLM-L6-v2")
qdrant = QdrantClient(host="localhost", port=6333)


def embed(text):
    return model.encode(text).tolist()


query = "air carrier liability"

results = qdrant.query_points(
    collection_name="legal_chunks",
    query=embed(query),
    limit=5
)

for r in results.points:
    print("\n---")
    print("DOC:", r.payload["doc_id"])
    print("ARTICLE:", r.payload["article"])
    print("TEXT:", r.payload["text"][:300])