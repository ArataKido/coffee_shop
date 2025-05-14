from fastapi import Depends, HTTPException
from typing import Optional
from datetime import datetime, timedelta, UTC
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import JWTError, jwt

from app.config import settings
from app.schemas.token import Token
from app.dependencies import get_user_service, get_oauth_scheme
from app.schemas.user import UserCreateSchema, UserSchema
from app.services.user_service import UserService
import logging

logger = logging.getLogger(__name__)
class AuthService:
    ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes
    SECRET_KEY = settings.secret_key
    ALGORITHM = settings.algorithm
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    oauth2_scheme: OAuth2PasswordBearer
    
    def __init__(self, user_service: UserService = Depends(get_user_service),
                oauth_scheme: OAuth2PasswordBearer = Depends(get_oauth_scheme)):
        self.user_service = user_service  
        self.oauth2_scheme = oauth_scheme

    async def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    async def get_password_hash(self, password: str) -> str:
        return self.pwd_context.hash(password)

    async def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        to_encode = data.copy()
        expire = datetime.now(UTC) + (expires_delta or timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)

    async def get_current_user(self, token: str = Depends(get_oauth_scheme)) -> UserSchema:
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            user_id = int(payload.get("sub"))  
            if user_id is None:
                raise HTTPException(status_code=401, detail="Could not validate credentials")
            return await self.user_service.get_user_by_id(user_id=user_id)  
        except JWTError:
            raise HTTPException(status_code=401, detail="Could not validate credentials")
        except Exception as e:
            logger.error(f"Error getting user with token {token}: {str(e)}") 

    async def signup(self, user_data: UserCreateSchema) -> UserSchema:
        existing_user = await self.user_service.get_user_by_email(user_data.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        user_data.password = await self.get_password_hash(user_data.password)
        return await self.user_service.create_user(user_data)

    async def login(self, username: str, password: str) -> Token:
        user = await self.user_service.get_user_for_auth(username)
        if not user or not await self.verify_password(password, user.password):
            raise HTTPException(status_code=400, detail="Incorrect username or password")
        access_token = await self.create_access_token(data={"sub": user.id})
        return Token(access_token=access_token, token_type="bearer")

    async def refresh_token(self, token: str) -> Token:
        current_user = await self.get_current_user(token)
        access_token = await self.create_access_token(data={"sub": current_user.id})
        return Token(access_token=access_token, token_type="bearer")
    
    async def activate_user(self, verification_token:str):
        return await self.user_service.activate_user(verification_token)