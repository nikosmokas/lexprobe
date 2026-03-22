from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import tempfile
import os

from app.rag.rag_pipeline import ask
from .mcp_agent import analyze_contract

app = FastAPI()

# ------------------------------
# CORS
# ------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow everything (dev mode)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------
# Existing /ask endpoint (RAG)
# ------------------------------
@app.get("/ask")
def query(q: str):
    answer = ask(q)
    return {"question": q, "answer": answer}

# ------------------------------
# New /upload endpoint
# ------------------------------
uploaded_docs = {}

@app.post("/upload")
async def upload_contract(file: UploadFile = File(...), user_prompt: str = Form(...)):
    # Save uploaded file temporarily
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=file.filename)
    content = await file.read()
    temp_file.write(content)
    temp_file.close()

    # Store file_id and prompt
    uploaded_docs[temp_file.name] = {"filename": file.filename, "prompt": user_prompt}

    return {"message": "File uploaded successfully", "file_id": temp_file.name}

# ------------------------------
# New /analyze endpoint
# ------------------------------
@app.post("/analyze")
async def analyze(file_id: str = Form(...)):
    if file_id not in uploaded_docs:
        return JSONResponse({"error": "File not found"}, status_code=404)

    doc_info = uploaded_docs[file_id]
    file_path = file_id
    user_prompt = doc_info["prompt"]

    try:
        result = analyze_contract(file_path, user_prompt)
        return {"answer": result}
    finally:
        # optional: remove temp file after analysis
        if os.path.exists(file_path):
            os.remove(file_path)
            uploaded_docs.pop(file_id, None)