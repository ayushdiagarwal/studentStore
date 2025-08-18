# app/schema/product.py
from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import List, Optional
from datetime import datetime

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    location: str
    category: str
    tags: Optional[List[str]] = []

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    location: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = None
    is_sold: Optional[bool] = None

class ProductResponse(ProductBase):
    id: str  # Changed from UUID to str
    date_added: Optional[datetime] = None
    seller_id: str  # Changed from UUID to str
    image_urls: List[str] = []
    is_sold: bool = False

    # Pydantic v2 config
    model_config = ConfigDict(from_attributes=True)

    # Ensure ObjectId or other types are cast to string for id
    @field_validator('id', mode='before')
    @classmethod
    def _cast_id_to_str(cls, value):
        return str(value) if value is not None else ""
