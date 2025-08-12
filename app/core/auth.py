import httpx
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt # for encoding/decoding jwt token
from app.core.config import settings
from app.models.user import User

# Google OAuth endpoints
GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[Dict[str, Any]]:
    """Verify and decode a JWT token"""
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except JWTError:
        return None

async def get_google_user_info(access_token: str) -> Optional[Dict[str, Any]]:
    """Get user information from Google using access token"""
    async with httpx.AsyncClient() as client:
        headers = {"Authorization": f"Bearer {access_token}"}
        response = await client.get(GOOGLE_USERINFO_URL, headers=headers)
        
        if response.status_code == 200:
            return response.json()
        return None

async def authenticate_google_user(google_user_info: Dict[str, Any]) -> User:
    """Authenticate or create a user from Google OAuth data"""
    email = google_user_info.get("email")
    oauth_id = google_user_info.get("id")
    
    if not email or not oauth_id:
        raise ValueError("Invalid Google user info")
    
    # Check if user already exists
    user = await User.find_one({"email": email})
    
    if user:
        # Update OAuth ID if not set
        if not user.oauth_id:
            user.oauth_id = oauth_id
            await user.save()
        return user
    
    # Create new user
    user_data = {
        "email": email,
        "name": google_user_info.get("name", ""),
        "profile_picture": google_user_info.get("picture"),
        "oauth_provider": "google",
        "oauth_id": oauth_id,
        "is_verified": True,  # Google accounts are pre-verified
        "is_active": True
    }
    
    user = User(**user_data)
    await user.insert()
    return user

def get_google_auth_url() -> str:
    """Generate Google OAuth authorization URL"""
    params = {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "scope": "openid email profile",
        "response_type": "code",
        "access_type": "offline",
        "prompt": "consent"
    }
    
    query_string = "&".join([f"{k}={v}" for k, v in params.items()])
    return f"{GOOGLE_AUTH_URL}?{query_string}"

async def exchange_code_for_token(code: str) -> Optional[Dict[str, Any]]:
    """Exchange authorization code for access token"""
    async with httpx.AsyncClient() as client:
        data = {
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": settings.GOOGLE_REDIRECT_URI
        }
        
        response = await client.post(GOOGLE_TOKEN_URL, data=data)
        
        if response.status_code == 200:
            return response.json()
        return None
