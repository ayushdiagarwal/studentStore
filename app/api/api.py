from fastapi import APIRouter
from app.api.endpoints import products, auth

# Create the main router
api_router = APIRouter()

# Include the router from the products endpoints
api_router.include_router(products.router, tags=["Products"])

# Include the authentication router
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])

# You will add other routers here later
# e.g., api_router.include_router(users.router, tags=["Users"])