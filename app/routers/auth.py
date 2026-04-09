from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.auth import (
    SignupRequest,
    LoginRequest,
    RefreshTokenRequest,
    TokenResponse
)
from app.schemas.user import UserResponse
from app.services.auth_service import AuthService
from app.utils.rate_limiter import limiter

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/signup", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")
async def signup(
    request: Request,
    signup_request: SignupRequest,
    db: Session = Depends(get_db)
):
    """Register a new user with email and password."""
    user, tokens = AuthService.signup(signup_request, db)
    return tokens

@router.post("/login", response_model=TokenResponse)
@limiter.limit("10/minute")
async def login(
    request: Request,
    login_request: LoginRequest,
    db: Session = Depends(get_db)
):
    """Authenticate a user and return JWT tokens."""
    user, tokens = AuthService.login(login_request, db)
    return tokens

@router.post("/refresh", response_model=TokenResponse)
@limiter.limit("10/minute")
async def refresh_token(
    request: Request,
    refresh_request: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    """Refresh an access token using a refresh token."""
    user, tokens = AuthService.refresh_access_token(refresh_request.refresh_token, db)
    return tokens

@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(request: Request):
    """
    Logout endpoint.
    
    Note: Since tokens are stateless (JWT), the client must discard the tokens on their end.
    This endpoint exists for API completeness and to signal logout intent to the backend.
    """
    return {
        "message": "Successfully logged out",
        "note": "Please discard tokens on the client side"
    }
