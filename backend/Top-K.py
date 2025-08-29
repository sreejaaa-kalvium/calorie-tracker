import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("API key not found. Ensure GOOGLE_API_KEY is set in the .env file.")

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-1.5-flash")

# Example: Set top_k in generation config
generation_config = {
    "top_k": 40,          # consider only the top 40 most likely tokens
    "temperature": 0.8,   # keep some creativity
    "top_p": 1.0,
    "max_output_tokens": 150
}

prompt = "Write a creative recipe for a healthy breakfast using oats."

response = model.generate_content(prompt, generation_config=generation_config)

print("AI Response with top_k=40:\n")
print(response.text)
