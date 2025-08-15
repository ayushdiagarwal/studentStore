from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class GoogleAuthRequest(BaseModel):
    """Schema for Google OAuth authorization request"""
    pass

class GoogleAuthCallback(BaseModel):
    """Schema for Google OAuth callback"""
    code: str
    state: Optional[str] = None

class TokenResponse(BaseModel):
    """Schema for authentication token response"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: "UserResponse"

class UserResponse(BaseModel):
    """Schema for user response"""
    id: str
    email: EmailStr
    name: str
    profile_picture: Optional[str] = None
    gender: Optional[str] = None
    hostel: Optional[str] = None
    is_verified: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    """Schema for creating a new user"""
    email: EmailStr
    name: str
    profile_picture: Optional[str] = None
    oauth_provider: str = "google"
    oauth_id: str

class UserUpdate(BaseModel):
    """Schema for updating user profile fields"""
    gender: Optional[str] = None
    hostel: Optional[str] = None

# Update forward references
TokenResponse.model_rebuild()
UserResponse.model_rebuild()
