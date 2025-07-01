from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.user import User
from app.schemas.user_schema import UserUpdateSchema
from app.repositories.base_repository import BaseRepository
from app.utils.security import get_password_hash

class UserRepository(BaseRepository):
    """Repository for user operations."""

    def __init__(self, db: AsyncSession):
        super().__init__(db, User)

    def get_all_admins_sync(self) -> list[User]:
        query = select(self.model_class).where(self.model_class.is_admin == True)
        result = self.db.execute(query)
        return result.scalars().all()

    async def patch_update_user(self, user_data:UserUpdateSchema, user:User) -> User:
        try:
            # Update fields if provided
            for field in ["username", "email", "is_admin", "is_active"]:
                value = getattr(user_data, field)
                if value is not None:
                    setattr(user, field, value)

            if user_data.password is not None:
                user.password = await get_password_hash(user_data.password)
            # Update and commit using the repository
            return await self.user_repo.update_and_commit(user)
        except Exception:
            self.logger.exception(f"Error updating user {user.id}")
            self.db.rollback()

