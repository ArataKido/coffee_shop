from sqlalchemy.ext.asyncio import AsyncSession
from app.models.category import Category
from app.schemas.category_schema import CategoryCreate, CategoryUpdate
from app.repositories.base_repository import BaseRepository


class CategoryRepository(BaseRepository):
    def __init__(self, db: AsyncSession):
        super().__init__(db, Category)

    async def create_category(self, category_data: CategoryCreate, creator_id: int) -> Category:
        category = self.category_repo.create_model(name=category_data.name, description=category_data.description)
        return await self.add_and_commit(category, created_by_user_id=creator_id)

    async def update_category(
        self, category: Category, category_update: CategoryUpdate, updater_id: int
    ) -> Category | None:
        try:
            if category_update.name is not None:
                category.name = category_update.name
            if category_update.description is not None:
                category.description = category_update.description
            if category_update.is_active is not None:
                category.is_active = category_update.is_active

            # Update in database
            await self.category_repo.update_and_commit(category, updated_by_user_id=updater_id)
            return category
        except Exception as e:
            self.logger.exception(f"Error updating category {category.id}: {e!s}")
            await self.db.rollback()
            return None
