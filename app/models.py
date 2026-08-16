from pydantic import BaseModel, Field
from typing import List


class ProductInput(BaseModel):
    product_name: str = Field(..., examples=["Handmade Leather Wallet"])
    category: str = Field(..., examples=["Fashion Accessories"])
    key_features: List[str] = Field(
        ..., examples=[["Genuine leather", "6 card slots", "Slim design"]]
    )
    target_platform: str = Field(
        default="Shopify", examples=["Shopify", "Amazon", "eBay"]
    )
    tone: str = Field(
        default="professional",
        examples=["professional", "playful", "luxury"],
    )


class ProductListing(BaseModel):
    title: str
    description: str
    seo_keywords: List[str]
    bullet_points: List[str]