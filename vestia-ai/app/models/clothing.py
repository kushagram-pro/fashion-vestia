from pydantic import BaseModel

class ClothingItem(BaseModel):
    id: str
    user_id: str
    type: str  # shirt, pants, shoes
    color: str
    style: str  # casual, formal, streetwear
    season: str