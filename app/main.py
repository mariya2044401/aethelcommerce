from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI, HTTPException
from app.models import ProductInput, ProductListing
from app.agent import generate_listing

app = FastAPI(
    title="AethelCommerce - Product Launch Agent",
    description="Product info se auto-generated e-commerce listing banata hai",
    version="0.1.0",
)


@app.get("/")
def health_check():
    return {"status": "ok", "agent": "product-launch-agent"}


@app.post("/generate-listing", response_model=ProductListing)
def create_listing(product: ProductInput):
    try:
        return generate_listing(product)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))