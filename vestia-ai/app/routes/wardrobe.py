from fastapi import APIRouter
from app.models.clothing import ClothingItem
from app.services.wardrobe_service import add_item, get_user_items

router = APIRouter()

@router.post("/add")
def add_clothing(item: ClothingItem):
    return add_item(item)

@router.get("/{user_id}")
def get_wardrobe(user_id: str):
    return get_user_items(user_id)