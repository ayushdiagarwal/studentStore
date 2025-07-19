# app/schema/product.py
from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID
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
    id: UUID
    date_added: datetime
    seller_id: UUID
    image_urls: List[str]
    is_sold: bool

    class Config:
        from_attributes = True
