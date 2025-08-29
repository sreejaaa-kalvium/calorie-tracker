import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get API key from .env
api_key = os.getenv("GOOGLE_API_KEY")

# Debug: Check if the API key is loaded
if not api_key:
    raise ValueError("API key not found. Ensure GOOGLE_API_KEY is set in the .env file.")

# Configure Gemini with the key
genai.configure(api_key=api_key)

# Use Gemini 1.5 Flash model
model = genai.get_model("models/gemini-1.5-flash")

# Zero-shot prompt
response = genai.generate_text(
    model=model,
    prompt="Summarize the story of Cinderella in three sentences."
)

print(response.text)