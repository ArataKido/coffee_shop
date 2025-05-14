from fastapi import Depends, HTTPException, status
from typing import Optional
from datetime import datetime, timedelta, UTC
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from app.config import settings
from app.schemas.token import Token
from app.dependencies.auth_dependencies import get_user_service, get_oauth_scheme
from app.schemas.user import UserCreateSchema, UserSchema
from app.services.user_service import UserService
from app.utils.security import get_password_hash, verify_password
import logging

logger = logging.getLogger(__name__)
class AuthService:
    ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes
    SECRET_KEY = settings.secret_key
    ALGORITHM = settings.algorithm
    oauth2_scheme: OAuth2PasswordBearer
    
    def __init__(self, 
                user_service: UserService = Depends(get_user_service),
                oauth_scheme: OAuth2PasswordBearer = Depends(get_oauth_scheme)
                ):
        self.user_service = user_service  
        self.oauth2_scheme = oauth_scheme
    

    async def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        to_encode = data.copy()
        expire = datetime.now(UTC) + (expires_delta or timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)

    async def decode_access_token(self, token: str) -> dict | None:
        """Decodes the JWT token and returns the payload."""
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except jwt.PyJWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials (JWT error)",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except Exception as e:
            raise logger.error(f"Error while decoding token {token}: {str(e)}")
        
    async def get_user_details_from_token_payload(self, payload: dict) -> UserSchema | None:
        """Helper to fetch user details based on token payload."""
        username = payload.get("sub")
        if username is None:
            return None

        user = await self.user_service.get_user_by_username(username=username)
        if user:

            return UserSchema.model_validate(user) 
        return None

    async def get_current_user_from_token(self, token: str) -> UserSchema:
        try:
            payload = await self.decode_access_token(token)
            if not payload:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")

            user = await self.get_user_details_from_token_payload(payload)
            if user is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
            
            # Check if user is active (assuming UserSchema has an is_active attribute)
            if not getattr(user, "is_active", True):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
            return user 
        except Exception as e:
            logger.error(f"Error getting user with token {token}: {str(e)}") 

    async def signup(self, user_data: UserCreateSchema) -> UserSchema:
        existing_user = await self.user_service.get_user_by_email(user_data.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        user_data.password = await get_password_hash(user_data.password)
        return await self.user_service.create_user(user_data)

    async def login(self, username: str, password: str) -> Token:
        user = await self.user_service.get_user_for_auth(username)
        if not user or not await verify_password(password, user.password):
            raise HTTPException(status_code=400, detail="Incorrect username or password")
        access_token = await self.create_access_token(data={"sub": user.username})
        return Token(access_token=access_token, token_type="bearer")

    async def refresh_token(self, token: str) -> Token:
        current_user = await self.get_current_user_from_token(token)
        access_token = await self.create_access_token(data={"sub": current_user.username})
        return Token(access_token=access_token, token_type="bearer")
    
    async def activate_user(self, verification_token:str):
        return await self.user_service.activate_user(verification_token)