from fastapi import APIRouter, Depends, Query, status, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.auth import TokenResponse
from app.services.oauth_service import OAuthService
from app.utils.rate_limiter import limiter

router = APIRouter(prefix="/oauth", tags=["oauth"])

@router.post("/google/callback", response_model=TokenResponse)
@limiter.limit("10/minute")
async def google_callback(
    request: Request,
    code: str = Query(...),
    db: Session = Depends(get_db)
):
    """Handle Google OAuth callback."""
    user, tokens = await OAuthService.handle_google_callback(code, db)
    return tokens

@router.post("/github/callback", response_model=TokenResponse)
@limiter.limit("10/minute")
async def github_callback(
    request: Request,
    code: str = Query(...),
    db: Session = Depends(get_db)
):
    """Handle GitHub OAuth callback."""
    user, tokens = await OAuthService.handle_github_callback(code, db)
    return tokens
