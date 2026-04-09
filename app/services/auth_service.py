from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.auth import SignupRequest, LoginRequest
from app.utils.password import hash_password, verify_password
from app.services.token_service import TokenService
from app.exceptions import (
    UserAlreadyExistsException,
    InvalidCredentialsException,
    UserNotFoundException
)

class AuthService:
    @staticmethod
    def signup(request: SignupRequest, db: Session):
        """Register a new user."""
        # Check if user already exists
        existing_user = db.query(User).filter(User.email == request.email).first()
        if existing_user:
            raise UserAlreadyExistsException()
        
        # Create new user
        user = User(
            email=request.email,
            hashed_password=hash_password(request.password),
            is_active=True,
            is_admin=False
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        
        # Generate tokens
        tokens = TokenService.generate_tokens(user)
        return user, tokens

    @staticmethod
    def login(request: LoginRequest, db: Session):
        """Authenticate a user."""
        user = db.query(User).filter(User.email == request.email).first()
        
        if not user or not verify_password(request.password, user.hashed_password):
            raise InvalidCredentialsException()
        
        if not user.is_active:
            raise InvalidCredentialsException()
        
        # Generate tokens
        tokens = TokenService.generate_tokens(user)
        return user, tokens

    @staticmethod
    def refresh_access_token(refresh_token: str, db: Session):
        """Generate a new access token using a refresh token."""
        from app.utils.jwt_handler import verify_token
        import uuid
        
        payload = verify_token(refresh_token)
        if not payload or payload.get("type") != "refresh":
            raise InvalidCredentialsException()
        
        user_id = payload.get("sub")
        if not user_id:
            raise InvalidCredentialsException()
        
        try:
            user_id_uuid = uuid.UUID(user_id)
        except ValueError:
            raise InvalidCredentialsException()
        
        user = db.query(User).filter(User.id == user_id_uuid).first()
        if not user:
            raise UserNotFoundException()
        
        # Generate new tokens
        tokens = TokenService.generate_tokens(user)
        return user, tokens
