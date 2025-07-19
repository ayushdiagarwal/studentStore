from fastapi import APIRouter
from app.api.endpoints import products

# Create the main router
api_router = APIRouter()

# Include the router from the products endpoints
api_router.include_router(products.router, tags=["Products"])

# You will add other routers here later
# e.g., api_router.include_router(users.router, tags=["Users"])
# e.g., api_router.include_router(auth.router, tags=["Authentication"])