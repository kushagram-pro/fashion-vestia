from fastapi import FastAPI
from app.routes import user, wardrobe, outfit

app = FastAPI()

app.include_router(user.router, prefix="/user")
app.include_router(wardrobe.router, prefix="/wardrobe")
app.include_router(outfit.router, prefix="/outfit")

@app.get("/")
def root():
    return {"message": "AI Stylist Backend Running"}