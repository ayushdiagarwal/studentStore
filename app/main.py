# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.api import api_router
from app.db.session import init_db
from app.core.cloudinary_config import init_cloudinary

app = FastAPI(title="Student Store API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite dev server
        "http://localhost:3000",  # Alternative React dev server
        "http://127.0.0.1:5173",  # Alternative localhost format
        "http://127.0.0.1:3000",  # Alternative localhost format
        "http://localhost:4173",  # Vite preview server
        "http://localhost:8080",  # Alternative port
    ],

    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
    expose_headers=["*"],  # Expose all headers
)

@app.get("/")
async def root():
    """
    Root endpoint providing API information.
    """
    return {
        "message": "Student Store API",
        "version": "1.0.0",
        "docs": "/docs",
        "api_base": "/api/v1"
    }

@app.on_event("startup")
async def on_startup():
    """
    Connect to the database and initialize Cloudinary when the application starts.
    """
    await init_db()
    init_cloudinary()

app.include_router(api_router, prefix="/api/v1")