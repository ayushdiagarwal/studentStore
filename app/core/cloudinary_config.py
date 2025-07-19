# app/core/cloudinary_config.py
import cloudinary
from app.core.config import settings

def init_cloudinary():
    """
    Initialize Cloudinary configuration using settings from config.
    """
    cloudinary.config(
        cloud_name=settings.CLOUDINARY_CLOUD_NAME,
        api_key=settings.CLOUDINARY_API_KEY,
        api_secret=settings.CLOUDINARY_API_SECRET,
        secure=True
    )
    print("Cloudinary configuration initialized...") 