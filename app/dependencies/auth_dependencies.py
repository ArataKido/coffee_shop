from typing_extensions import deprecated
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserSchema
from app.services.auth_service import AuthService
from app.services.user_service import UserService
from app.utils.security import oauth2_scheme


@deprecated("This DI dependency is deprecated, use the providers and container instead")
async def get_db_session(session: AsyncSession = Depends(get_db)) -> AsyncSession:
    return session


@deprecated("This DI dependency is deprecated, use the providers and container instead")
async def get_user_repository(db: AsyncSession = Depends(get_db_session)) -> UserRepository:
    return UserRepository(db=db)


@deprecated("This DI dependency is deprecated, use the providers and container instead")
async def get_user_service(user_repo: UserRepository = Depends(get_user_repository)) -> UserService:
    return UserService(db=user_repo.db, user_repository=user_repo)


@deprecated("This DI dependency is deprecated, use the providers and container instead")
async def get_auth_service(user_service: UserService = Depends(get_user_service)) -> AuthService:
    return AuthService(user_service=user_service, oauth_scheme=oauth2_scheme)


@deprecated("This DI dependency is deprecated, use the providers and container instead")
async def get_current_active_user(
    token: str = Depends(oauth2_scheme), auth_service: AuthService = Depends(get_auth_service)
) -> UserSchema: 
    user = await auth_service.get_current_user_from_token(token=token)
    return user


@deprecated("This DI dependency is deprecated, use the providers and container instead")
async def user_is_admin(current_user: UserSchema = Depends(get_current_active_user)) -> UserSchema:
    if not getattr(current_user, "is_admin", False):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access forbidden: Admins only")
    return current_user
