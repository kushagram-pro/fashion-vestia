from pydantic import BaseModel

class User(BaseModel):
    id: str
    name: str
    age: int
    gender: str
    style_preference: str