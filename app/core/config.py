# app/core/config.py
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database Configuration - Use local MongoDB for development
    DATABASE_URL: str = "mongodb://localhost:27017/student_store"
    
    # Cloudinary Configuration
    CLOUDINARY_CLOUD_NAME: str = ""
    CLOUDINARY_API_KEY: str = ""
    CLOUDINARY_API_SECRET: str = ""
    
    # Google OAuth Configuration
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    GOOGLE_REDIRECT_URI: str = "http://localhost:8002/api/v1/auth/google/callback"
    
    # JWT Configuration
    JWT_SECRET_KEY: str = "your-secret-key-change-this-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")

settings = Settings()

# Validate required settings
def validate_settings():
    """Validate that required settings are configured"""
    if not settings.GOOGLE_CLIENT_ID:
        print("⚠️  WARNING: GOOGLE_CLIENT_ID is not set. Google OAuth will not work.")
        print("   Please create a .env file with your Google OAuth credentials.")
    
    if not settings.GOOGLE_CLIENT_SECRET:
        print("⚠️  WARNING: GOOGLE_CLIENT_SECRET is not set. Google OAuth will not work.")
    
    if not settings.JWT_SECRET_KEY or settings.JWT_SECRET_KEY == "your-secret-key-change-this-in-production":
        print("⚠️  WARNING: JWT_SECRET_KEY is using default value. Change this in production.")
    
    print(f"📊 Database URL: {settings.DATABASE_URL}")
    print(f"🔐 Google OAuth: {'✅ Configured' if settings.GOOGLE_CLIENT_ID else '❌ Not configured'}")

# Call validation on import
validate_settings()