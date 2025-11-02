"""
Authentication routes
"""
from fastapi import APIRouter, HTTPException, Depends, status
from .auth_models import UserLogin, UserRegister, Token, UserResponse
from ..services.auth_service import auth_service
from ..core.security import get_current_user

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserRegister):
    """
    Register a new user
    
    - **username**: Unique username (3-50 characters)
    - **password**: Password (minimum 6 characters)
    - **email**: Email address (optional)
    - **full_name**: Full name (optional)
    """
    user_id = auth_service.create_user(
        username=user_data.username,
        password=user_data.password,
        email=user_data.email,
        full_name=user_data.full_name
    )
    
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists or registration failed"
        )
    
    user = auth_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="User created but could not be retrieved"
        )
    
    return UserResponse(**user)


@router.post("/login", response_model=Token)
async def login(credentials: UserLogin):
    """
    Login with username and password
    
    Returns JWT access token for authenticated requests
    """
    result = auth_service.login(credentials.username, credentials.password)
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return Token(**result)


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """
    Get current authenticated user information
    
    Requires: Bearer token in Authorization header
    """
    user = auth_service.get_user_by_id(current_user["user_id"])
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return UserResponse(**user)


@router.post("/logout")
async def logout(current_user: dict = Depends(get_current_user)):
    """
    Logout current user
    
    Note: JWT tokens are stateless, so logout is handled client-side
    by removing the token. This endpoint confirms the token is valid.
    """
    return {
        "status": "success",
        "message": f"User {current_user['username']} logged out successfully"
    }
