import os
from dotenv import load_dotenv
from google import genai
from .prompt import build_prompt

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def generate_answer(question, contexts):
    prompt = build_prompt(question, contexts)

    print(f"Prompt length: {len(prompt)} chars")

    response = client.models.generate_content(
        model="gemini-3-flash-preview",  # Use correct model name
        contents=prompt,
        config={"temperature": 0.2, "max_output_tokens": 300}
    )

    return response.text