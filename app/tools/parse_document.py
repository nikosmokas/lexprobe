import re
from docx import Document
import PyPDF2


def clean_text(text):
    """Clean text by normalizing whitespace"""
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def parse_document(file_path: str) -> str:
    """
    Extract text from PDF, DOCX, or TXT file
    """
    text = ""
    if file_path.endswith(".pdf"):
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            text = "\n".join([page.extract_text() for page in reader.pages])
    elif file_path.endswith(".docx"):
        doc = Document(file_path)
        text = "\n".join([p.text for p in doc.paragraphs])
    elif file_path.endswith(".txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
    else:
        raise ValueError("Unsupported file type")

    # Clean the extracted text
    return clean_text(text)