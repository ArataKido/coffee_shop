from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from app.models.user import User as UserModel
from app.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository):
    """Repository for user operations."""

    def __init__(self, db: AsyncSession ):
        super().__init__(db, UserModel)

    def get_all_admins_sync(self) -> list[UserModel]:
        query = select(self.model_class).where(self.model_class.is_admin == True)
        result = self.db.execute(query)
        return result.scalars().all()
