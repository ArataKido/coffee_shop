from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from datetime import datetime

class UserBaseSchema(BaseModel):
    """Base DTO for user data."""
    username: str
    email: EmailStr

    # Modern way to configure Pydantic models for ORM support
    model_config = ConfigDict(from_attributes=True)

class UserCreateSchema(UserBaseSchema):
    """DTO for creating a new user."""
    password: str


class UserSchema(UserBaseSchema):
    """DTO for user response data."""
    id: int
    created_at: datetime
    updated_at: datetime
    is_active: bool
    is_admin: Optional[bool] = False
    

class UserUpdateSchema(BaseModel):
    """DTO for updating an existing user."""
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)
