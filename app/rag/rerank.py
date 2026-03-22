from sentence_transformers import CrossEncoder

# 🔥 cross-encoder = true reranker (better than embeddings)
reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")


def rerank(query, results, top_k=3):
    pairs = [(query, r["text"]) for r in results]

    scores = reranker.predict(pairs)

    # attach scores
    for i, r in enumerate(results):
        r["rerank_score"] = float(scores[i])

    # sort by rerank score
    ranked = sorted(results, key=lambda x: x["rerank_score"], reverse=True)

    return ranked[:top_k]