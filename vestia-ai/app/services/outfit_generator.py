from app.services.wardrobe_service import get_user_items

def generate_outfit(user_id: str):
    items = get_user_items(user_id)

    tops = [i for i in items if i["type"] == "shirt"]
    bottoms = [i for i in items if i["type"] == "pants"]

    if not tops or not bottoms:
        return {"error": "Not enough items"}

    return {
        "top": tops[0],
        "bottom": bottoms[0]
    }