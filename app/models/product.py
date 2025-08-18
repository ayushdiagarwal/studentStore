# app/models/product.py
from beanie import Document
from pydantic import Field
from typing import List, Optional, Any
from datetime import datetime
from bson import ObjectId

class Product(Document):
    # Let Beanie handle the _id field automatically
    name: str
    description: Optional[str] = None
    price: float
    date_added: datetime = Field(default_factory=datetime.utcnow)
    seller_id: str  # MongoDB ObjectId as string
    image_urls: List[str] = []
    location: str
    category: str
    tags: Optional[List[str]] = []
    is_sold: bool = False

    # No conversion hooks needed; we now persist clean string IDs only

    class Settings:
        name = "products"

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "iPhone 12",
                "description": "Great condition, barely used",
                "price": 599.99,
                "location": "University Campus",
                "category": "Electronics",
                "tags": ["phone", "apple", "electronics"]
            }
        }
    }

    class Settings:
        name = "products"  # This is the name of the MongoDB collection