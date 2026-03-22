from dotenv import load_dotenv
load_dotenv()


import json
from tqdm import tqdm
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance

INPUT_FILE = "../data/processed/legal_chunks.jsonl"
COLLECTION_NAME = "legal_chunks"

# 🔥 local model
model = SentenceTransformer("all-MiniLM-L6-v2")  # 384 dims

qdrant = QdrantClient(host="localhost", port=6333)


def create_collection():
    if not qdrant.collection_exists(COLLECTION_NAME):
        qdrant.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE),
        )

def embed(text):
    return model.encode(text).tolist()


def run():
    create_collection()

    points = []
    idx = 0

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        for line in tqdm(f):
            item = json.loads(line)

            vector = embed(item["text"])

            points.append({
                "id": idx,
                "vector": vector,
                "payload": item
            })

            idx += 1

            if len(points) >= 100:
                qdrant.upsert(
                    collection_name=COLLECTION_NAME,
                    points=points
                )
                points = []

    if points:
        qdrant.upsert(
            collection_name=COLLECTION_NAME,
            points=points
        )

    print("✅ DONE: vectors stored")


if __name__ == "__main__":
    run()