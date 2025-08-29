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

# Example: set temperature in generation config
generation_config = {
    "temperature": 0.9,   # controls creativity
    "top_p": 1.0,
    "max_output_tokens": 150
}

prompt = "Write a short poem about healthy eating."

response = model.generate_content(prompt, generation_config=generation_config)

print("AI Response with temperature=0.9:\n")
print(response.text)
