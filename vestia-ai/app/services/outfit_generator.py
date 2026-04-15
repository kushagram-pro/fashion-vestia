import json
import re
from app.core.ollama_client import query_ollama
from app.utils.color_matcher import score_palette

def rank_items_by_color(wardrobe):
    """
    Sort items based on how well they match each other
    """

    scored = []

    for item in wardrobe:
        total_score = 0

        for other in wardrobe:
            if item == other:
                continue

            score = score_palette(
                item.get("palette", []),
                other.get("palette", [])
            )

            total_score += score

        scored.append((item, total_score))

    scored.sort(key=lambda x: x[1], reverse=True)

    return [item for item, _ in scored]

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
    try:
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            return match.group(0)
        return None
    except:
        return None

def safe_parse_json(text):

    cleaned = text.replace("```json", "").replace("```", "").strip()
    json_str = extract_first_json(cleaned)

    if not json_str:
        return {"error": "No JSON found", "raw": text}

    try:
        return json.loads(json_str)
    except Exception as e:
        return {
            "error": "Failed to parse AI response",
            "raw": json_str,
            "exception": str(e)
        }

def generate_outfit(wardrobe, user_profile, occasion, weather):

    if not wardrobe:
        return {"error": "Wardrobe is empty"}

    wardrobe = rank_items_by_color(wardrobe)
    prompt = build_prompt(wardrobe, user_profile, occasion, weather)

    response = query_ollama(prompt)

    if isinstance(response, dict) and "error" in response:
        return response

    parsed = safe_parse_json(response)

    return parsed