# app/db/session.py
import motor.motor_asyncio
from beanie import init_beanie
from app.core.config import settings
from app.models.product import Product # We will create this model next

async def init_db():
    """
    Initializes the database connection and Beanie ODM.
    """
    client = motor.motor_asyncio.AsyncIOMotorClient(
        settings.DATABASE_URL
    )
    
    # Initialize Beanie with the Product document model
    await init_beanie(database=client.get_default_database(), document_models=[Product])
    print("Database connection initialized...")