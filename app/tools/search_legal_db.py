from typing import List, Dict
from ..rag.retrieve import retrieve


def search_legal_db(contract_text: str) -> List[Dict]:
    """
    Retrieve relevant legal references from the vector DB based on contract content
    """
    # Extract key terms from contract text for better search
    key_terms = []
    text_lower = contract_text.lower()

    # Basic contract terms
    if "liability" in text_lower:
        key_terms.append("liability")
    if "non-disclosure" in text_lower or "confidential" in text_lower:
        key_terms.append("non-disclosure agreement")
    if "term" in text_lower:
        key_terms.append("contract term")
    if "termination" in text_lower:
        key_terms.append("termination")
    if "governing law" in text_lower or "jurisdiction" in text_lower:
        key_terms.append("governing law")

    # EU-specific legal terms
    if "gdpr" in text_lower or "data protection" in text_lower:
        key_terms.append("data protection")
    if "personal data" in text_lower:
        key_terms.append("personal data")
    if "data subject" in text_lower:
        key_terms.append("data subject rights")
    if "germany" in text_lower or "german" in text_lower:
        key_terms.append("german law")
    if "eu" in text_lower or "european" in text_lower:
        key_terms.append("european union")

    if not key_terms:
        key_terms = ["contract", "agreement"]

    # Use the most relevant terms as query
    query = " ".join(key_terms[:4])  # e.g., "liability non-disclosure agreement data protection governing law"

    results = retrieve(query, k=5)  # Get top 5 results
    return results