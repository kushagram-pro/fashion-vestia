from fastapi import APIRouter
from app.services.outfit_generator import generate_outfit

router = APIRouter()

@router.get("/{user_id}")
def get_outfit(user_id: str):
    return generate_outfit(user_id)