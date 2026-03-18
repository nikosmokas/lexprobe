import os
from dotenv import load_dotenv
import google.generativeai as genai
from .prompt import build_prompt

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-3-flash-preview")


def generate_answer(question, contexts):
    prompt = build_prompt(question, contexts)

    response = model.generate_content(prompt)

    return response.text