import tempfile
from typing import List, Dict

from ..tools.parse_document import parse_document
from ..tools.search_legal_db import search_legal_db
from ..tools.risk_analysis import risk_analysis
from ..rag.utils import compute_confidence

# ------------------------------
# MCP Agent
# ------------------------------

def analyze_contract(file_path: str, user_prompt: str) -> Dict:
    """
    Multi-component pipeline:
    1. Parse document
    2. Retrieve relevant legal references
    3. Analyze for risks
    4. Return structured answer
    """
    contract_text = parse_document(file_path)
    legal_refs = search_legal_db(contract_text)
    risks = risk_analysis(contract_text, legal_refs)

    answer = {
        "title": f"Analysis of {file_path.split('/')[-1]}",
        "points": [
            f"Contract has {len(risks)} potential risk(s).",
            *[f"Clause: {r['clause']} → Risk: {r['risk']}" for r in risks]
        ],
        "sources": legal_refs,
        "confidence": compute_confidence(legal_refs)
    }

    return answer