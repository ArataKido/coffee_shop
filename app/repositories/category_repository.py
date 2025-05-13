from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import List, Optional

from app.models.category import Category
from app.repositories.base_repository import BaseRepository


class CategoryRepository(BaseRepository):
    def __init__(self, db: AsyncSession):
        super().__init__(db, Category)
    
    async def find_by_name(self, name: str) -> Optional[Category]:
        """Find a category by name"""
        query = select(Category).where(Category.name == name, Category.is_active == True)
        result = await self.db.execute(query)
        return result.scalars().first()
    
    async def find_all_active(self) -> List[Category]:
        """Find all active categories"""
        query = select(Category).where(Category.is_active == True)
        result = await self.db.execute(query)
        return result.scalars().all()
        
