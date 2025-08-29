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

# Example prompt
user_input = "Summarize the story of Snow White in two sentences."

response = model.generate_content(user_input)

# Print response
print("AI Response:", response.text)

# --- Token Logging ---
# Count tokens by estimating from input + output
# Gemini doesn't expose exact token usage yet, so we use length approximation
input_tokens = len(user_input.split())
output_tokens = len(response.text.split())
total_tokens = input_tokens + output_tokens

print(f"Input tokens (approx): {input_tokens}")
print(f"Output tokens (approx): {output_tokens}")
print(f"Total tokens (approx): {total_tokens}")
