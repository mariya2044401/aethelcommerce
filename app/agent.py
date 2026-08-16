import os
import json
from google import genai
from app.models import ProductInput, ProductListing

MODEL_NAME = "gemini-3.1-flash-lite"

_client = None


def get_client() -> genai.Client:
    global _client
    if _client is None:
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError(
                "GEMINI_API_KEY set nahi hai. .env file check karo."
            )
        _client = genai.Client(api_key=api_key)
    return _client


SYSTEM_INSTRUCTIONS = """\
Tum ek e-commerce product listing expert ho. Tumhein product info di jayegi
aur tumhein sirf JSON format mein reply karna hai, koi extra text nahi.

JSON shape:
{
  "title": "SEO-friendly product title, 60 characters se kam",
  "description": "2-3 paragraph persuasive description",
  "seo_keywords": ["keyword1", "keyword2", ...],
  "bullet_points": ["benefit 1", "benefit 2", ...]
}
"""


def build_prompt(data: ProductInput) -> str:
    return f"""
Product Name: {data.product_name}
Category: {data.category}
Key Features: {", ".join(data.key_features)}
Target Platform: {data.target_platform}
Tone: {data.tone}

Upar diye gaye data se ek complete product listing banao, JSON format mein.
"""


def generate_listing(data: ProductInput) -> ProductListing:
    client = get_client()
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=build_prompt(data),
        config={
            "system_instruction": SYSTEM_INSTRUCTIONS,
            "response_mime_type": "application/json",
        },
    )

    raw_text = response.text
    parsed = json.loads(raw_text)

    return ProductListing(
        title=parsed["title"],
        description=parsed["description"],
        seo_keywords=parsed["seo_keywords"],
        bullet_points=parsed["bullet_points"],
    )