# app/models/product.py
from beanie import Document
from pydantic import Field
from typing import List, Optional
from uuid import UUID, uuid4
from datetime import datetime

class Product(Document):
    id: UUID = Field(default_factory=uuid4, alias="_id")
    name: str
    description: Optional[str] = None
    price: float
    date_added: datetime = Field(default_factory=datetime.utcnow)
    seller_id: UUID  # In a real app, this would be a Link to a User document
    image_urls: List[str] = []
    location: str
    category: str
    tags: Optional[List[str]] = []
    is_sold: bool = False

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