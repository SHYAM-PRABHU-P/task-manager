from google import genai
import json
import re

client = genai.Client(api_key="AIzaSyDMjO0OFtf9HTbKvBXDqY-ErokljGxa_NA")

def extract_intent(user_input):
    prompt = f"""
You are a JSON API.

STRICT RULES:
- Output ONLY JSON
- No explanation
- No markdown
- No extra text

Valid intents: reminder, todo, note, query

User input: "{user_input}"

Return JSON exactly in this format:
{{
  "intent": "",
  "task": "",
  "time": ""
}}
"""

    response = client.models.generate_content(
        model="models/gemini-flash-latest",
        contents=prompt
    )

    raw = response.text.strip()

    # 🔐 FIX 2: Extract JSON safely
    match = re.search(r"\{.*\}", raw, re.DOTALL)
    if not match:
        raise ValueError("No JSON found in Gemini response")

    return json.loads(match.group())

