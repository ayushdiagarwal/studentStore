from fastapi import APIRouter, HTTPException, Depends, status, Response
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import RedirectResponse
from app.schema.auth import GoogleAuthRequest, GoogleAuthCallback, TokenResponse, UserResponse, UserUpdate
from app.core.auth import (
    get_google_auth_url,
    exchange_code_for_token,
    get_google_user_info,
    authenticate_google_user,
    create_access_token,
    verify_token
)
from app.models.user import User
from datetime import timedelta
from app.core.config import settings

router = APIRouter()
security = HTTPBearer()

@router.get("/google/login", response_model=dict)
async def google_login():
    """
    Get Google OAuth authorization URL
    """
    try:
        auth_url = get_google_auth_url()
        return {"auth_url": auth_url}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate Google auth URL: {str(e)}"
        )

@router.get("/google/callback")
async def google_callback(code: str, state: str = None):
    """
    Handle Google OAuth callback and authenticate user
    """
    try:
        # Exchange authorization code for access token
        token_data = await exchange_code_for_token(code)
        if not token_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to exchange code for token"
            )
        
        access_token = token_data.get("access_token")
        if not access_token:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No access token received from Google"
            )
        
        # Get user info from Google using the access token
        google_user_info = await get_google_user_info(access_token)
        if not google_user_info:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to get user info from Google"
            )
        
        # Authenticate or create user
        user = await authenticate_google_user(google_user_info)
        
        # Create JWT token
        token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(user.id), "email": user.email},
            expires_delta=token_expires
        )
        
        # Redirect to frontend with token and user data as query parameters
        frontend_url = "http://localhost:5173/auth/success"
        redirect_url = f"{frontend_url}?token={access_token}&user_id={user.id}&email={user.email}&name={user.name}"
        
        return RedirectResponse(url=redirect_url)
        
    except HTTPException:
        raise
    except Exception as e:
        # Redirect to frontend with error
        error_url = f"http://localhost:5173/auth/error?error={str(e)}"
        return RedirectResponse(url=error_url)

@router.get("/me", response_model=UserResponse)
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Get current authenticated user information
    """
    try:
        token = credentials.credentials
        payload = verify_token(token)
        
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        user = await User.get(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Inactive user"
            )
        
        return UserResponse(
            id=str(user.id),
            email=user.email,
            name=user.name,
            profile_picture=user.profile_picture,
            gender=user.gender,
            hostel=user.hostel,
            is_verified=user.is_verified,
            created_at=user.created_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get user info: {str(e)}"
        )

@router.patch("/me", response_model=UserResponse)
async def update_current_user(update: UserUpdate, credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Update current authenticated user's profile (gender/hostel)
    """
    try:
        token = credentials.credentials
        payload = verify_token(token)
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload",
                headers={"WWW-Authenticate": "Bearer"},
            )

        user = await User.get(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        dirty = False
        if update.gender is not None:
            user.gender = update.gender
            dirty = True
        if update.hostel is not None:
            user.hostel = update.hostel
            dirty = True

        if dirty:
            await user.update_timestamp()

        return UserResponse(
            id=str(user.id),
            email=user.email,
            name=user.name,
            profile_picture=user.profile_picture,
            gender=user.gender,
            hostel=user.hostel,
            is_verified=user.is_verified,
            created_at=user.created_at,
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update user info: {str(e)}"
        )

# logout is simply handled by the frontend.
@router.post("/logout")
async def logout():
    """
    Logout endpoint (client should discard the token)
    """
    return {"message": "Successfully logged out"}
