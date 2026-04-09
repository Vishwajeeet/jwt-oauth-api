from datetime import timedelta
from sqlalchemy.orm import Session
from app.models.user import User
from app.utils.jwt_handler import create_access_token, create_refresh_token

class TokenService:
    @staticmethod
    def generate_tokens(user: User):
        """Generate access and refresh tokens for a user."""
        access_token_expires = timedelta(minutes=15)
        access_token = create_access_token(
            data={"sub": str(user.id)},
            expires_delta=access_token_expires
        )
        refresh_token = create_refresh_token(data={"sub": str(user.id)})
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }
