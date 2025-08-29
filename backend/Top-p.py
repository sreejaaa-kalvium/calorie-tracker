import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("API key not found. Ensure GOOGLE_API_KEY is set in the .env file.")

genai.configure(api_key=api_key)

# Configure model with Top P
model = genai.GenerativeModel("gemini-1.5-flash")

# Set generation config (with top_p)
generation_config = {
    "top_p": 0.3,       # nucleus sampling threshold
    "temperature": 0.7, # optional, controls randomness further
    "max_output_tokens": 150
}

prompt = "Write a creative description of a sunset over the mountains."

response = model.generate_content(prompt, generation_config=generation_config)

print("AI Response with top_p=0.3:\n", response.text)
