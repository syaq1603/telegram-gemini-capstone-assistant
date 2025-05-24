# assistant.py

import os
import google.generativeai as genai
from dotenv import load_dotenv
import markdown

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-pro")

system_prompt = """
You are a helpful assistant with expertise in finance, economics, investing, and financial markets.

Only answer questions that are directly related to these topics.

If a user asks something unrelated — such as programming, movies, recipes, or personal issues — respond with:
"I'm only able to help with questions about finance, economics, investing, and financial markets."
"""

def generate_financial_reply(prompt: str) -> str:
    full_prompt = [
        {"role": "system", "parts": [system_prompt.strip()]},
        {"role": "user", "parts": [prompt.strip()]}
    ]
    try:
        response = model.generate_content(full_prompt)
        raw_text = response.text or "I'm only able to help with questions about finance, economics, investing, and financial markets."
        html_output = markdown.markdown(raw_text, extensions=["fenced_code", "codehilite"])

        print("\n--- QUERY LOG ---")
        print(f"User Prompt: {prompt}")
        print(f"Gemini Response: {raw_text}")
        print("--- END LOG ---\n")

        return html_output
    except Exception as e:
        print(f"Gemini Error: {e}")
        return f"⚠️ Error: {str(e)}"
