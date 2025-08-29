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

# --- Dynamic Prompting Example ---
user_input = "2 boiled eggs and 1 slice of bread"

dynamic_prompt = f"""
You are a nutrition assistant.
The user will provide a meal description, and you must estimate the total calories clearly.
User input: {user_input}
Respond with: 'Your meal has approximately X calories.'
"""

response = model.generate_content(dynamic_prompt)

print(response.text)
