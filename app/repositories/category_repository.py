from sqlalchemy.ext.asyncio import AsyncSession

from app.models.category import Category
from app.repositories.base_repository import BaseRepository


class CategoryRepository(BaseRepository):
    def __init__(self, db: AsyncSession):
        super().__init__(db, Category)
