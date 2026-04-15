import json
import uuid
import os
from fastapi import UploadFile

from app.services.image_analyzer import analyze_image
from app.utils.color_extractor import extract_colors

FILE_PATH = "app/data/wardrobe.json"
UPLOAD_DIR = "uploads"


# Ensure upload folder exists
os.makedirs(UPLOAD_DIR, exist_ok=True)


def load_data():
    with open(FILE_PATH, "r") as f:
        return json.load(f)


def save_data(data):
    with open(FILE_PATH, "w") as f:
        json.dump(data, f, indent=4)


def save_image(file: UploadFile, item_id: str):
    ext = file.filename.split(".")[-1]
    file_path = os.path.join(UPLOAD_DIR, f"{item_id}.{ext}")

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    return file_path


def add_item(user_id: str, file: UploadFile):
    """
    Upload image → analyze → store enriched clothing data
    """

    item_id = str(uuid.uuid4())

    # Step 1: Save image locally
    image_path = save_image(file, item_id)

    # Step 2: Analyze image using LLaVA
    analysis = analyze_image(image_path)

    # Step 2.5: Extract colors
    colors = extract_colors(image_path)

    if "error" in analysis:
        return {"error": "Image analysis failed", "details": analysis}

    # Step 3: Build item
    item = {
        "id": item_id,
        "user_id": user_id,
        "image_path": image_path,
        "label": analysis.get("label", "garment"),
        "category": analysis.get("category", "unknown"),
        "color": analysis.get("color", "unknown"),
        "palette": colors,
        "style": analysis.get("style", "unknown"),
        "fit": analysis.get("fit", "unknown"),
        "season": analysis.get("season", "unknown")
    }

    # Step 4: Save to DB
    data = load_data()
    data.append(item)
    save_data(data)

    return item


def get_user_items(user_id: str):
    data = load_data()
    return [item for item in data if item["user_id"] == user_id]


def delete_item(item_id: str):
    data = load_data()
    new_data = [item for item in data if item["id"] != item_id]
    save_data(new_data)

    return {"message": "Item deleted"}