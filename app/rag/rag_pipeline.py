from .retrieve import retrieve
from .generate import generate_answer

def ask(question: str):
    contexts = retrieve(question)
    answer = generate_answer(question, contexts)
    return answer