from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict

from app.services.outfit_generator import generate_outfit

router = APIRouter()

class OutfitRequest(BaseModel):
    wardrobe : List[Dict]
    user_profile: Dict
    occasion: str
    weather : str

@router.post("/generate-outfit")
def generate_outfit_api(request: OutfitRequest):
    """
    Main endpoint to generate outfit using AI
    """
    outfit = generate_outfit(
        wardrobe=request.wardrobe,
        user_profile=request.user_profile,
        occasion=request.occasion,
        weather=request.weather
    )
    return {"outfit": outfit}