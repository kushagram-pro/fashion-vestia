import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

MODEL = "phi3"  # 🔥 switch to phi3 for structured output


def query_ollama(prompt: str):
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "format": "json",  # 🔥 THIS IS THE GAME CHANGER
        "options": {
            "temperature": 0.2,   # 🔥 reduce creativity
            "top_p": 0.9
        }
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload)

        if response.status_code != 200:
            return {"error": response.text}

        data = response.json()

        return data.get("response", "")

    except Exception as e:
        return {"error": str(e)}