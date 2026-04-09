from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import uuid

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

class TaskResponse(BaseModel):
    id: uuid.UUID
    title: str
    description: Optional[str] = None
    owner_id: uuid.UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class TaskDetailResponse(TaskResponse):
    owner: Optional['UserResponse'] = None

from app.schemas.user import UserResponse
TaskDetailResponse.update_forward_refs()
