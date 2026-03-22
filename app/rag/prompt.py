from .context_builder import format_contexts


def build_prompt(question, contexts):
    context_block = format_contexts(contexts)

    return f"""
You are a legal assistant.

Answer the question using ONLY the context below.
If unsure, say "Not enough information".

QUESTION:
{question}

CONTEXT:
{context_block}

INSTRUCTIONS:
- Be concise
- Use bullet points
- Cite articles like (Article X, DOC_ID)
- No fluff

ANSWER:
"""