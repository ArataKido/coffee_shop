from fastapi import HTTPException, status
from jose import ExpiredSignatureError, JWTError, jwt
from datetime import UTC, datetime, timedelta

from app.config import Config
from app.schemas.token_schema import Token
from app.schemas.user_schema import UserCreateSchema, UserSchema
from app.services.user_service import UserService
from app.utils.security import get_password_hash, verify_password
from app.utils.loggers.logger import Logger



class AuthService:

    def __init__(self, user_service: UserService, logger:Logger, app_config:Config):
        self.user_service = user_service
        self.logger = logger
        self.app_config = app_config.app


    async def create_access_token(self, data: dict, expires_delta: timedelta | None = None) -> str:
        """
        _summary_

        Args:
            data (dict): _description_
            expires_delta (Optional[timedelta], optional): _description_. Defaults to None.

        Returns:
            str: _description_

        """
        to_encode = data.copy()
        expire = datetime.now(UTC) + (expires_delta or timedelta(minutes=self.app_config.access_token_expire_minutes))
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.app_config.secret_key, algorithm=self.app_config.algorithm)

    async def decode_access_token(self, token: str) -> dict | None:
        """Decodes the JWT token and returns the payload."""
        try:
            payload = jwt.decode(token, self.app_config.secret_key, algorithms=[self.app_config.algorithm])
            return payload
        except ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials (JWT error)",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except Exception as e:
            raise self.logger.error(f"Error while decoding token {token}: {e!s}")

    async def get_user_details_from_token_payload(self, payload: dict) -> UserSchema | None:
        """
        Helper to fetch user details based on token payload.

        Returns:
            _type_: _description_

        """
        username = payload.get("sub")
        if username is None:
            return None

        user = await self.user_service.get_user_by_username(username=username)
        if user:
            return UserSchema.model_validate(user)
        return None

    async def get_current_user_from_token(self, token: str) -> UserSchema:
        """
        Gets user information for token

        Args:
            token (str): JWT token

        Returns:
            UserSchema: contains user information

        """
        try:
            payload = await self.decode_access_token(token)
            if not payload:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")

            user = await self.get_user_details_from_token_payload(payload)
            if user is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

            if not getattr(user, "is_active", True):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
            return user
        except Exception as e:
            self.logger.exception(f"Error getting user with token {token}: {e!s}")

    async def signup(self, user_data: UserCreateSchema) -> UserSchema:
        """
        Method for signing up user

        Args:
            user_data (UserCreateSchema): contains user information used for signing up

        Returns:
            UserSchema:  contains user information

        """
        existing_user = await self.user_service.get_user_by_email(user_data.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        user_data.password = await get_password_hash(user_data.password)
        return await self.user_service.create_user(user_data)

    async def login(self, username: str, password: str) -> Token:
        """
        Method for authenticating user

        Args:
            username
            password
        Returns:
            Token: JWT token, used for authenticating

        """
        user = await self.user_service.get_user_for_auth(username)
        if not user or not await verify_password(password, user.password):
            raise HTTPException(status_code=400, detail="Incorrect username or password")
        access_token = await self.create_access_token(data={"sub": user.username})
        return Token(access_token=access_token, token_type="bearer")

    async def refresh_token(self, token: str) -> Token:
        """
        Method for refreshing access token

        Args:
            token (str): JWT token

        Returns:
            Token: JWT token, used for authenticating

        """
        current_user = await self.get_current_user_from_token(token)
        access_token = await self.create_access_token(data={"sub": current_user.username})
        return Token(access_token=access_token, token_type="bearer")

    async def activate_user(self, verification_token: str):
        return await self.user_service.activate_user(verification_token)

