from .retrieve import retrieve
from .generate import generate_answer
from .utils import compute_confidence, extract_sources


def ask(question: str):
    results = retrieve(question)

    answer = generate_answer(question, results)

    sources = extract_sources(results)
    confidence = compute_confidence(results)

    return {
        "question": question,
        "answer": answer,
        "sources": sources,
        "confidence": confidence
    }