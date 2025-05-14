from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from sqlalchemy import select as sync_select
from app.repositories.base_repository import BaseRepository
from app.models.user import User as UserModel
from app.schemas.user import UserCreateSchema, UserSchema, UserUpdateSchema
from typing import Optional, List, Union


class UserRepository(BaseRepository[UserModel]):
    """Repository for user operations."""
    
    def __init__(self, db: Union[AsyncSession, Session]):
        super().__init__(db, UserModel)
    

    def get_all_admins_sync(self) -> List[UserModel]:
        query = select(self.model_class).where(self.model_class.is_admin == True)
        result =  self.db.execute(query)
        return result.scalars().all()
    



