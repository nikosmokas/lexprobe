def build_prompt(question: str, contexts: list):
    context_text = "\n\n".join([
        f"{c['article']} ({c['doc_id']}): {c['text']}"
        for c in contexts
    ])

    return f"""
You are a legal assistant specialized in EU law.

Answer the question using ONLY the context below.
Cite articles and document IDs.

Context:
{context_text}

Question:
{question}

Answer:
"""