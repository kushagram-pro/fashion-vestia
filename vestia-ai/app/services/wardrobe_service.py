import json
import uuid
from app.models.clothing import ClothingItem

FILE_PATH = "app/data/wardrobe.json"

def load_data():
    with open(FILE_PATH, "r") as f:
        return json.load(f)

def save_data(data):
    with open(FILE_PATH, "w") as f:
        json.dump(data, f, indent=4)

def add_item(item: ClothingItem):
    data = load_data()
    item_dict = item.dict()
    item_dict["id"] = str(uuid.uuid4())
    data.append(item_dict)
    save_data(data)
    return item_dict

def get_user_items(user_id: str):
    data = load_data()
    return [item for item in data if item["user_id"] == user_id]