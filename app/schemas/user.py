from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List
import uuid

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class UserResponse(BaseModel):
    id: uuid.UUID
    email: str
    is_active: bool
    is_admin: bool
    created_at: datetime

    class Config:
        from_attributes = True

class UserDetailResponse(UserResponse):
    oauth_accounts: List['OAuthAccountResponse'] = []

class OAuthAccountResponse(BaseModel):
    id: uuid.UUID
    provider: str
    account_id: str
    account_email: str

    class Config:
        from_attributes = True

UserDetailResponse.update_forward_refs()
