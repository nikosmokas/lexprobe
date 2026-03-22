def clean_text(text: str, max_chars=600):
    # remove legal noise
    text = text.replace("Whereas:", "")
    text = text.replace("HAS DECIDED AS FOLLOWS:", "")

    # collapse whitespace
    text = " ".join(text.split())

    return text[:max_chars]


def format_contexts(contexts):
    formatted = []

    for c in contexts:
        formatted.append(
            f"{c.get('article', '')} ({c.get('doc_id', '')}): {clean_text(c.get('text', ''))}"
        )

    return "\n".join(formatted)
