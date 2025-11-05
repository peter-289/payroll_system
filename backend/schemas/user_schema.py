from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    full_name: str = Field(..., min_length=1, max_length=100)
    status: Optional[str] = 'inactive'


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserResponse(UserBase):
    user_id: int
    role_id: Optional[int] = None
    last_login: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    is_active: bool = False
    message: Optional[str] = None

    model_config = {"from_attributes": True}