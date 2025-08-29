# backend/structured_output.py
"""
Structured Output Example using Google Gemini (genai).

Requirements:
    pip install google-generativeai python-dotenv fastapi uvicorn pydantic

Usage:
    - Put your GOOGLE_API_KEY in backend/.env (or root .env)
    - Run: uvicorn structured_output:app --reload --port 8000
"""

import os
import json
from typing import List, Optional
from pydantic import BaseModel, ValidationError
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
import google.generativeai as genai
import time

# Load env
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise RuntimeError("GOOGLE_API_KEY not found in backend/.env")

genai.configure(api_key=API_KEY)
MODEL_NAME = "gemini-1.5-flash"

app = FastAPI(title="Calorie Tracker - Structured Output")

# --- Pydantic schema that matches expected structured output ---
class Item(BaseModel):
    name: str
    quantity: str
    calories: float
    note: Optional[str] = None

class StructuredEstimate(BaseModel):
    total_calories: float
    items: List[Item]
    confidence: float  # 0.0 - 1.0
    explanation: str

# --- System prompt instructing the model to RETURN JSON only ---
SYSTEM_PROMPT = """
You are a nutrition assistant. The user will provide a meal description.
Return ONLY valid JSON that exactly matches the schema described below (no explanation).
Schema:
{
  "total_calories": number,
  "items": [
    { "name": string, "quantity": string, "calories": number, "note": string|null }
  ],
  "confidence": number,        // between 0.0 and 1.0
  "explanation": string        // one-sentence summary
}
If uncertain about exact calories, estimate and lower the confidence. Use metric/US units inferred
from the user's text. Keep explanation to one short sentence.
"""

def approx_token_count(text: str) -> int:
    # Simple token approximation: whitespace-splitting (not exact but usable for logs)
    return len(text.split())

def call_gemini_for_structured(user_input: str, generation_config: dict = None) -> dict:
    """
    Ask Gemini to return JSON that matches our schema.
    We do some defensive parsing to extract JSON from the response.
    """
    if generation_config is None:
        generation_config = {
            "top_p": 0.95,
            "temperature": 0.0,
            "max_output_tokens": 450
        }

    start_time = time.time()
    model = genai.GenerativeModel(MODEL_NAME)

    # Compose final prompt
    user_prompt = f"Estimate calories for: {user_input}"

    resp = model.generate_content(
        SYSTEM_PROMPT + "\n\n" + user_prompt,
        generation_config=generation_config
    )

    elapsed = time.time() - start_time

    # Try to robustly extract JSON:
    text = resp.text.strip()
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1:
        raise RuntimeError("Model did not return JSON. Raw response: " + text)

    json_str = text[start:end+1]
    try:
        data = json.loads(json_str)
    except json.JSONDecodeError as e:
        # If model included trailing commas or comments, try to clean common issues:
        cleaned = json_str.replace(",}", "}").replace(",]", "]")
        data = json.loads(cleaned)  # may still raise

    # Logging approximate token usage and timing
    input_tokens = approx_token_count(SYSTEM_PROMPT + " " + user_prompt)
    output_tokens = approx_token_count(text)
    total_tokens = input_tokens + output_tokens
    print(f"[Gemini] elapsed={elapsed:.2f}s approximate_tokens_in={input_tokens} out={output_tokens} total={total_tokens}")

    return data

@app.post("/structured-estimate", response_model=StructuredEstimate)
def structured_estimate(body: dict):
    """
    POST body example:
    { "text": "I ate 2 bananas, 1 cup of whole milk, and a slice of toast with butter." }
    """
    text = body.get("text", "")
    if not text or not text.strip():
        raise HTTPException(status_code=400, detail="`text` required in request body")

    try:
        raw_data = call_gemini_for_structured(text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Model error: {e}")

    # Validate & coerce to StructuredEstimate via Pydantic
    try:
        structured = StructuredEstimate.parse_obj(raw_data)
    except ValidationError as ve:
        # Return helpful error with model output for debugging (but avoid leaking keys in prod)
        raise HTTPException(status_code=500, detail=f"Invalid structured output: {ve.errors()} | raw: {raw_data}")

    return structured

@app.get("/health")
def health():
    return {"status": "ok"}
