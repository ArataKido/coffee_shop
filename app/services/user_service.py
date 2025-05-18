from base64 import b64decode, b64encode

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.config import settings
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreateSchema, UserSchema, UserUpdateSchema, UserWithPassword
from app.utils.security import get_password_hash
from app.utils.tasks import check_user_status_task, send_verification_email_task
from app.utils.loggers.logger import Logger

logger = Logger()


class UserService:
    """
    Service layer for user operations.
    This demonstrates the proper way to use repositories in a layered architecture.
    """

    def __init__(self, db: AsyncSession | Session, user_repository: UserRepository):
        self.db = db
        self.user_repo = user_repository

    async def get_user_by_id(self, user_id: int) -> UserSchema | None:
        """Get a user by their ID."""
        try:
            user = await self.user_repo.find_by(id=user_id)
            return UserSchema.model_validate(user) if user else None
        except Exception as e:
            logger.exception(f"Error getting user by ID {user_id}: {e!s}")
            return None

    async def get_user_by_username(self, username: str) -> UserSchema | None:
        """Get a user by their ID."""
        try:
            user = await self.user_repo.find_by(username=username)
            return UserSchema.model_validate(user) if user else None
        except Exception as e:
            logger.exception(f"Error getting user by username {username}: {e!s}")
            return None

    async def get_user_for_auth(self, username: str) -> UserWithPassword | None:
        """
        WARNING: Use this method only for internal operations.
        Do not return the result by API
        """
        try:
            user = await self.user_repo.find_by(username=username)
            return UserWithPassword.model_validate(user) if user else None
        except Exception as e:
            logger.exception(f"Error getting user by username {username}: {e!s}")
            return None

    # Синхронная версия для Celery
    def get_user_by_id_sync(self, user_id: int) -> UserSchema | None:
        """Get a user by their ID (sync version for Celery)."""
        try:
            user = self.user_repo.find_by_sync(id=user_id)
            return UserSchema.model_validate(user) if user else None
        except Exception as e:
            logger.exception(f"Error getting user by ID {user_id}: {e!s}")
            return None

    async def get_user_by_email(self, email: str) -> UserSchema | None:
        """Get a user by their email."""
        try:
            user = await self.user_repo.find_by(email=email)
            return UserSchema.model_validate(user) if user else None
        except Exception as e:
            logger.exception(f"Error getting user by email {email}: {e!s}")
            return None

    async def get_all_users(self) -> list[UserSchema]:
        """Get all active users."""
        try:
            users = await self.user_repo.get_all()
            return [UserSchema.model_validate(user) for user in users]
        except Exception as e:
            logger.exception(f"Error getting all users: {e!s}")
            return []

    def get_admin_emails_sync(self) -> list[str] | None:
        try:
            admins = self.user_repo.get_all_admins_sync()

            return [admin.email for admin in admins]
        except Exception as e:
            logger.exception(f"Error getting admin emails: {e!s}")
            return None

    async def create_user(self, user_data: UserCreateSchema, creator_id: int | None = None) -> UserSchema | None:
        """Create a new user."""
        try:
            # Check if email already exists
            existing_user = await self.user_repo.find_by(email=user_data.email)
            if existing_user:
                logger.warning(f"User with email {user_data.email} already exists")
                return None

            # Create user using repository factory method
            user = self.user_repo.create_model(
                username=user_data.username,
                email=user_data.email,
                password=user_data.password,  # In real app, hash this!
            )

            # Save user to database
            created_user = await self.user_repo.add_and_commit(user, created_by_user_id=creator_id)
            await self.process_user_action(created_user.email, created_user.id)
            return UserSchema.model_validate(created_user)
        except Exception as e:
            logger.exception(f"Error creating user: {e!s}")
            # You might want to handle transaction rollback here if necessary
            await self.db.rollback()
            return None

    async def patch_update_user(self, user_id: int, user_data: UserUpdateSchema) -> UserSchema | None:
        """
        Patch update method for user.
        I would prefer generic method for all models, but because
        I am short on time, I wrote this method.
        """
        try:
            user = await self.user_repo.find_by(id=user_id)
            if not user:
                logger.warning(f"User with ID {user_id} not found")
                return None

            if user_data.username is not None:
                user.username = user_data.username
            if user_data.email is not None:
                user.email = user_data.email
            if user_data.password is not None:
                user.password = await get_password_hash(user_data.password)  # Hash password if updating
            if user_data.is_admin is not None:
                user.is_admin = user_data.is_admin
            if user_data.is_active is not None:
                user.is_active = user_data.is_active

            # Update and commit using the repository
            updated_user = await self.user_repo.update_and_commit(user)
            return UserSchema.model_validate(updated_user)
        except Exception as e:
            logger.exception(f"Error updating user {user_id}: {e!s}")
            await self.db.rollback()
            return None

    async def activate_user(self, verification_token: str) -> bool:
        try:
            user_id = await self._decode_verification_token(verification_token)
            user = await self.user_repo.find_by_id(user_id)
            if not user:
                logger.warning(f"User with ID {user_id} not found for activation")

            await self.user_repo.activate(user)
            await self.db.commit()
            return True
        except Exception as e:
            logger.exception(f"Error activating user with verification token {verification_token}: {e!s}")
            await self.db.rollback()
            return False

    async def soft_delete_user(self, user_id: int, deactivator_id: int | None = None) -> bool:
        """Soft delete a user by setting is_active to False."""
        try:
            user = await self.user_repo.find_by_id(user_id)
            if not user:
                logger.warning(f"User with ID {user_id} not found for deactivation")
                return False

            await self.user_repo.soft_delete(user, deleted_by_user_id=deactivator_id)
            await self.db.commit()
            return True
        except Exception as e:
            logger.exception(f"Error deactivating user {user_id}: {e!s}")
            await self.db.rollback()
            return False

    async def delete_user(self, user_id: int) -> bool:
        try:
            await self.user_repo.permanent_delete(user_id)
            await self.db.commit()
            return True
        except Exception as e:
            logger.exception(f"Error deleting user {user_id}: {e!s}")
            await self.db.rollback()
            return False

    # Синхронная версия для Celery
    def delete_user_sync(self, user_id: int) -> bool:
        try:
            self.user_repo.permanent_delete_sync(user_id)
            self.db.commit()
            return True
        except Exception as e:
            logger.error(f"Error deleting user {user_id}: {e!s}")
            self.db.rollback()
            return False

    async def process_user_action(self, user_email: int, user_id: int) -> None:
        token = await self._generate_verification_token(user_id)
        send_verification_email_task.apply_async(args=[user_email, token])

        check_user_status_task.apply_async(args=[user_id], countdown=settings.user_delete_timeout)

    async def is_user_active(self, user_id: int) -> bool:
        user = await self.get_user_by_id(user_id)
        return user.is_active if user else False

    # Синхронная версия для Celery
    def is_user_active_sync(self, user_id: int) -> bool:
        user = self.get_user_by_id_sync(user_id)
        return user.is_active if user else False

    async def _generate_verification_token(self, user_id: int):
        return b64encode(str(user_id).encode("utf-8")).decode("utf-8")

    async def _decode_verification_token(self, token: int | str):
        decoded_bytes = b64decode(token.encode("utf-8"))  # Decode base64
        decoded_string = decoded_bytes.decode("utf-8")
        return int(decoded_string)
