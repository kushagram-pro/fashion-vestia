import requests
import base64
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llava"


def encode_image(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def analyze_image(image_path):
    """
    Sends image to LLaVA and returns structured clothing data
    """

    image_base64 = encode_image(image_path)

    prompt = """
Analyze this clothing item.

Return ONLY valid JSON:

{
  "label": "short descriptive name",
  "category": "top | bottom | shoes | accessory | outerwear",
  "color": "main color",
  "style": "casual | formal | streetwear | sporty | ethnic",
  "fit": "slim | regular | oversized",
  "season": "summer | winter | all-season"
}
"""

    payload = {
        "model": MODEL,
        "prompt": prompt,
        "images": [image_base64],
        "stream": False,
        "format": "json",
        "options": {
            "temperature": 0.2
        }
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload)

        if response.status_code != 200:
            return {"error": response.text}

        data = response.json()
        result = data.get("response", "")

        return safe_parse_json(result)

    except Exception as e:
        return {"error": str(e)}


def safe_parse_json(text):
    try:
        return json.loads(text)
    except:
        text = text.replace("```json", "").replace("```", "").strip()
        try:
            return json.loads(text)
        except:
            return {"error": "Failed to parse", "raw": text}