from fastapi import FastAPI
from app.rag.rag_pipeline import ask

app = FastAPI()

@app.get("/ask")
def query(q: str):
    answer = ask(q)
    return {"question": q, "answer": answer}