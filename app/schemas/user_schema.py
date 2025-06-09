from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


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
    is_admin: bool | None = False


class UserWithPassword(UserSchema):
    password: str


class UserUpdateSchema(BaseModel):
    """DTO for updating an existing user."""

    username: str | None = None
    email: EmailStr | None = None
    password: str | None = None
    is_active: bool | None = None
    is_admin: bool | None = None

    model_config = ConfigDict(from_attributes=True)
