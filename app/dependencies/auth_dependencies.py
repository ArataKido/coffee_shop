# In: app/auth_dependencies.py

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

# Import service CLASS definitions
from app.services.auth_service import AuthService
from app.services.user_service import UserService
from app.schemas.user import UserSchema # Your Pydantic user schema

# Import repository CLASS definitions and DB session provider (adjust paths as needed)
from app.repositories.user_repository import UserRepository 
from app.db import get_db # Assuming get_db yields an SQLAlchemy session
from sqlalchemy.ext.asyncio import AsyncSession

# --- Helper Dependency: Database Session ---
async def get_db_session(session: AsyncSession = Depends(get_db)) -> AsyncSession:
    return session

# --- Helper Dependency: Repositories (Example for UserRepository) ---
async def get_user_repository(db: AsyncSession = Depends(get_db_session)) -> UserRepository:
    return UserRepository(db=db)

# --- Helper Dependency: Services (Example for UserService) ---
async def get_user_service(user_repo: UserRepository = Depends(get_user_repository)) -> UserService:
    # Adjust constructor based on your actual UserService
    return UserService(user_repository=user_repo) 

# --- Core Authentication Dependencies ---

# OAuth2 scheme (can be defined here or imported if defined globally)
# Ensure the tokenUrl matches your login endpoint
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login") 

# Dependency to provide an AuthService instance
async def get_auth_service(
    user_service: UserService = Depends(get_user_service) # AuthService depends on UserService
) -> AuthService:
    return AuthService(user_service=user_service)

# Dependency to get the currently authenticated and active user

async def get_current_active_user(
    token: str = Depends(oauth2_scheme),
    auth_service: AuthService = Depends(get_auth_service)
) -> UserSchema: # Return type should be your User schema
    # This now calls the method on the AuthService instance
    user = await auth_service.get_current_user_from_token(token=token)
    return user

# --- Admin-Specific Dependency (Your Goal) ---
async def user_is_admin(
    current_user: UserSchema = Depends(get_current_active_user)
) -> UserSchema:
    # Assuming your UserSchema has an 'is_admin' boolean attribute
    if not getattr(current_user, "is_admin", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden: Admins only"
        )
    return current_user