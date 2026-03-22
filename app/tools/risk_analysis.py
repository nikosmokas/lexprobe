from typing import List, Dict
from ..rag.generate import client


def risk_analysis(contract_text: str, legal_refs: List[Dict]) -> List[Dict]:
    """
    Analyze contract clauses for potential risks using LLM
    """
    # Prepare context from legal refs
    context_text = "\n".join([f"{ref.get('article', '')} ({ref.get('doc_id', '')}): {ref.get('text', '')}" for ref in legal_refs])

    # Create risk analysis prompt - try very simple approach
    risk_prompt = f"""Please review this contract and identify any potential problems or risks:

{contract_text[:800]}

What issues do you see? Be specific and explain your concerns. Use plain text format only - no markdown, no bullet points, no headers. Just write in normal paragraphs."""

    print(f"Risk analysis prompt length: {len(risk_prompt)} chars")

    # Use Gemini 3 Flash Preview (correct model name)
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=risk_prompt,
        config={"temperature": 0.3, "max_output_tokens": 2000}
    )

    # Extract text from response - be more thorough
    analysis = ""
    if hasattr(response, 'text') and response.text:
        analysis = response.text
    elif hasattr(response, 'candidates') and response.candidates:
        candidate = response.candidates[0]
        if hasattr(candidate, 'content'):
            if isinstance(candidate.content, str):
                analysis = candidate.content
            elif hasattr(candidate.content, 'parts'):
                parts = candidate.content.parts
                analysis = ''.join([part.text for part in parts if hasattr(part, 'text')])
            else:
                analysis = str(candidate.content)
        else:
            analysis = str(candidate)
    else:
        analysis = str(response)

    print(f"Final extracted analysis length: {len(analysis)} chars")
    if len(analysis) < 500:
        print(f"WARNING: Analysis is very short! Full response: {repr(analysis)}")

    # Simple approach: just return the raw LLM response as one risk
    # Don't overcomplicate with parsing - let the LLM do the formatting
    if analysis.strip():
        risks = [{"clause": "Contract Analysis", "risk": analysis.strip()}]
    else:
        risks = [{"clause": "Contract Analysis", "risk": "No analysis available."}]

    return risks