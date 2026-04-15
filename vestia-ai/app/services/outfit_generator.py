import json
import re
from app.core.ollama_client import query_ollama

def build_prompt(wardrobe, user_profile, occasion, weather):

    garment_list = [
    {
        "index": i,
        "label": item.get("label", item.get("type", "garment")),
        "category": item.get("category", item.get("type", "unknown")),
        "color": item.get("color", "unknown")
    }
    for i, item in enumerate(wardrobe)
    ]

    prompt = f"""
Return ONLY valid JSON.

Wardrobe:
{json.dumps(garment_list)}

User:
{json.dumps(user_profile)}

Occasion: {occasion}
Weather: {weather}

Generate outfit using given items.

Output format:
{{
  "outfitName": "...",
  "selectedItems": [
    {{
      "index": 0,
      "role": "...",
      "why": "..."
    }}
  ],
  "styleScore": "85%",
  "reasoningParagraph": "...",
  "colorStory": ["#000000"],
  "styleTips": [
    {{"icon": "✦", "tip": "..."}}
  ]
}}
"""
    return prompt

def extract_first_json(text):
    """
    Extracts the FIRST valid JSON object from messy LLM output
    """
    try:
        # find first { ... }
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            return match.group(0)
        return None
    except:
        return None

def safe_parse_json(text):
    """
    Robust parser for broken LLM outputs
    """

    # Step 1: clean markdown junk
    cleaned = text.replace("```json", "").replace("```", "").strip()

    # Step 2: extract first JSON block
    json_str = extract_first_json(cleaned)

    if not json_str:
        return {"error": "No JSON found", "raw": text}

    # Step 3: try parsing
    try:
        return json.loads(json_str)
    except Exception as e:
        return {
            "error": "Failed to parse AI response",
            "raw": json_str,
            "exception": str(e)
        }

def generate_outfit(wardrobe, user_profile, occasion, weather):
    """
    Main function used by API
    """

    if not wardrobe:
        return {"error": "Wardrobe is empty"}
    
    prompt = build_prompt(wardrobe, user_profile, occasion, weather)
    response = query_ollama(prompt)

    if isinstance(response, dict) and "error" in response:
        return response
    
    parsed = safe_parse_json(response)
    return parsed

