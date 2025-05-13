from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from sqlalchemy import select as sync_select
from app.repositories.base_repository import BaseRepository
from app.models.user import User as UserModel
from app.schemas.user import UserCreateSchema
from typing import Optional, List, Union


class UserRepository(BaseRepository[UserModel]):
    """Repository for user operations."""
    
    def __init__(self, db: Union[AsyncSession, Session]):
        super().__init__(db, UserModel)
    
    async def get_by_email(self, email: str) -> Optional[UserModel]:
        """Find a user by email."""
        return await self.find_one_by(email=email)
    
    # Синхронная версия для Celery
    def get_by_email_sync(self, email: str) -> Optional[UserModel]:
        """Find a user by email (sync version)."""
        return self.find_one_by_sync(email=email)
    
    async def get_by_user_id(self, account_id: int) -> List[UserModel]:
        """Get all records for a specific account."""
        result = await self.db.execute(
            select(self.model_class).filter(self.model_class.account_id == account_id)
        )
        return result.scalars().all()


