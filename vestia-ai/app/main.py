from fastapi import FastAPI
from app.routes import outfit

app = FastAPI()

app.include_router(outfit.router, prefix="/outfit")


@app.get("/")
def root():
    return {"message": "VESTIA AI running"}