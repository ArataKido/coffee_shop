from dishka.integrations.fastapi import FromDishka, inject
from typing_extensions import deprecated
from fastapi import Depends, HTTPException, status

from app.schemas.user_schema import UserSchema
from app.services.auth_service import AuthService
from app.utils.security import oauth2_scheme

@inject
async def get_current_active_user(
    auth_service:FromDishka[AuthService],
    token: str = Depends(oauth2_scheme),
) -> UserSchema:
    # auth_service = AuthService()
    user = await auth_service.get_current_user_from_token(token=token)
    return user


async def user_is_admin(current_user: UserSchema = Depends(get_current_active_user)) -> UserSchema:
    if not getattr(current_user, "is_admin", False):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access forbidden: Admins only")
    return current_user
