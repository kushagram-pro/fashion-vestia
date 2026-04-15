from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict

from app.services.outfit_generator import generate_outfit
from app.services.wardrobe_service import get_user_items

router = APIRouter()


class OutfitRequest(BaseModel):
    user_id: str
    user_profile: Dict
    occasion: str
    weather: str


@router.post("/generate")
def generate_outfit_api(request: OutfitRequest):

    # 🔥 Fetch wardrobe automatically
    wardrobe = get_user_items(request.user_id)

    if not wardrobe:
        return {"error": "No wardrobe items found for this user"}

    result = generate_outfit(
        wardrobe=wardrobe,
        user_profile=request.user_profile,
        occasion=request.occasion,
        weather=request.weather
    )

    return result