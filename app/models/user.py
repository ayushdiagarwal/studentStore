from beanie import Document, Indexed
from typing import Optional
from datetime import datetime
from pydantic import EmailStr, Field

class User(Document):
    email: Indexed(EmailStr, unique=True)
    name: str
    profile_picture: Optional[str] = None
    oauth_provider: str = "google"  # For future extensibility
    oauth_id: Optional[str] = None
    is_active: bool = True
    is_verified: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "users"
    
    class Config:
        schema_extra = {
            "example": {
                "email": "user@example.com",
                "name": "John Doe",
                "profile_picture": "https://example.com/avatar.jpg",
                "oauth_provider": "google",
                "oauth_id": "123456789",
                "is_active": True,
                "is_verified": True
            }
        }
    
    async def update_timestamp(self):
        """Update the updated_at timestamp"""
        self.updated_at = datetime.utcnow()
        await self.save()
