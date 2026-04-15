from fastapi import FastAPI
from app.routes import wardrobe, outfit

app = FastAPI()

# Phase 1 routes
app.include_router(wardrobe.router, prefix="/wardrobe")

# Phase 2 routes
app.include_router(outfit.router, prefix="/outfit")


@app.get("/")
def root():
    return {"message": "VESTIA AI running 🚀"}