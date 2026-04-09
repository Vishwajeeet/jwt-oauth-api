from sqlalchemy.orm import Session
from authlib.integrations.httpx_client import AsyncOAuth2Client
import httpx
from app.models.user import User, OAuthAccount
from app.config import settings
from app.services.token_service import TokenService
from app.exceptions import OAuthProviderException
import uuid

class OAuthService:
    GOOGLE_TOKEN_URL = "https://oauth.googleapis.com/token"
    GOOGLE_USERINFO_URL = "https://openidconnect.googleapis.com/v1/userinfo"
    
    GITHUB_TOKEN_URL = "https://github.com/login/oauth/access_token"
    GITHUB_USERINFO_URL = "https://api.github.com/user"
    
    @staticmethod
    async def handle_google_callback(code: str, db: Session):
        """Handle Google OAuth callback."""
        if not settings.GOOGLE_CLIENT_ID or not settings.GOOGLE_CLIENT_SECRET:
            raise OAuthProviderException("Google OAuth is not configured")
        
        try:
            # Exchange code for token
            token_response = httpx.post(
                OAuthService.GOOGLE_TOKEN_URL,
                data={
                    "code": code,
                    "client_id": settings.GOOGLE_CLIENT_ID,
                    "client_secret": settings.GOOGLE_CLIENT_SECRET,
                    "redirect_uri": f"{settings.FRONTEND_URL}/auth/callback/google",
                    "grant_type": "authorization_code"
                }
            )
            token_response.raise_for_status()
            tokens = token_response.json()
            
            # Get user info
            userinfo_response = httpx.get(
                OAuthService.GOOGLE_USERINFO_URL,
                headers={"Authorization": f"Bearer {tokens['access_token']}"}
            )
            userinfo_response.raise_for_status()
            userinfo = userinfo_response.json()
            
            return OAuthService.create_or_get_user(
                provider="google",
                account_id=userinfo["sub"],
                account_email=userinfo["email"],
                db=db
            )
        
        except Exception as e:
            raise OAuthProviderException(f"Google OAuth error: {str(e)}")
    
    @staticmethod
    async def handle_github_callback(code: str, db: Session):
        """Handle GitHub OAuth callback."""
        if not settings.GITHUB_CLIENT_ID or not settings.GITHUB_CLIENT_SECRET:
            raise OAuthProviderException("GitHub OAuth is not configured")
        
        try:
            # Exchange code for token
            token_response = httpx.post(
                OAuthService.GITHUB_TOKEN_URL,
                data={
                    "client_id": settings.GITHUB_CLIENT_ID,
                    "client_secret": settings.GITHUB_CLIENT_SECRET,
                    "code": code,
                    "redirect_uri": f"{settings.FRONTEND_URL}/auth/callback/github"
                },
                headers={"Accept": "application/json"}
            )
            token_response.raise_for_status()
            tokens = token_response.json()
            
            # Get user info
            userinfo_response = httpx.get(
                OAuthService.GITHUB_USERINFO_URL,
                headers={"Authorization": f"Bearer {tokens['access_token']}"}
            )
            userinfo_response.raise_for_status()
            userinfo = userinfo_response.json()
            
            return OAuthService.create_or_get_user(
                provider="github",
                account_id=str(userinfo["id"]),
                account_email=userinfo.get("email") or userinfo.get("login"),
                db=db
            )
        
        except Exception as e:
            raise OAuthProviderException(f"GitHub OAuth error: {str(e)}")
    
    @staticmethod
    def create_or_get_user(provider: str, account_id: str, account_email: str, db: Session):
        """Create a new user or return existing user for OAuth account."""
        # Check if OAuth account already exists
        oauth_account = db.query(OAuthAccount).filter(
            OAuthAccount.provider == provider,
            OAuthAccount.account_id == account_id
        ).first()
        
        if oauth_account:
            user = oauth_account.user
        else:
            # Check if user with email exists
            user = db.query(User).filter(User.email == account_email).first()
            
            if not user:
                # Create new user
                user = User(
                    email=account_email,
                    hashed_password=None,
                    is_active=True,
                    is_admin=False
                )
                db.add(user)
                db.flush()
            
            # Create OAuth account
            oauth_account = OAuthAccount(
                user_id=user.id,
                provider=provider,
                account_id=account_id,
                account_email=account_email
            )
            db.add(oauth_account)
            db.commit()
            db.refresh(user)
        
        # Generate tokens
        tokens = TokenService.generate_tokens(user)
        return user, tokens
