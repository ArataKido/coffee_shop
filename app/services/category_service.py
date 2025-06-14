from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.category_repository import CategoryRepository
from app.schemas.category_schema import CategoryCreate, CategoryInDB, CategoryUpdate
from app.utils.loggers.logger import Logger



class CategoryService:
    def __init__(self, db: AsyncSession, category_repository: CategoryRepository, logger:Logger):
        self.db = db
        self.category_repo = category_repository
        self.logger = logger

    async def get_category_by_id(self, category_id: int) -> CategoryInDB | None:
        """Get category by ID"""
        try:
            category = await self.category_repo.find_by_id(category_id)
            return CategoryInDB.model_validate(category) if category else None
        except Exception as e:
            self.logger.exception(f"Error getting category by ID {category_id}: {e!s}")
            return None

    async def get_all_categories(self) -> list[CategoryInDB]:
        """Get all categories"""
        try:
            categories = await self.category_repo.get_all()
            return [CategoryInDB.model_validate(cat) for cat in categories]
        except Exception as e:
            self.logger.exception(f"Error getting all categories: {e!s}")
            return []

    async def create_category(
        self, category_data: CategoryCreate, creator_id: int | None = None
    ) -> CategoryInDB | None:
        """Create a new category"""
        try:
            # Check if category with the same name already exists
            existing_category = await self.category_repo.find_by(name=category_data.name, is_active=True)
            if existing_category:
                self.logger.warning(f"Category with name {category_data.name} already exists")
                return None

            # Create category
            category = self.category_repo.create_model(name=category_data.name, description=category_data.description)

            created_category = await self.category_repo.add_and_commit(category, created_by_user_id=creator_id)
            return CategoryInDB.model_validate(created_category)
        except Exception as e:
            self.logger.exception(f"Error creating category: {e!s}")
            await self.db.rollback()
            return None

    async def update_category(
        self, category_id: int, category_data: CategoryUpdate, updater_id: int | None = None
    ) -> CategoryInDB | None:
        """Update a category"""
        try:
            # Get existing category
            category = await self.category_repo.find_by_id(category_id)
            if not category:
                self.logger.warning(f"Category with ID {category_id} not found")
                return None

            # Update fields if provided
            if category_data.name is not None:
                category.name = category_data.name
            if category_data.description is not None:
                category.description = category_data.description
            if category_data.is_active is not None:
                category.is_active = category_data.is_active

            # Update in database
            await self.category_repo.update(category, updated_by_user_id=updater_id)
            await self.db.commit()
            return CategoryInDB.model_validate(category)
        except Exception as e:
            self.logger.exception(f"Error updating category {category_id}: {e!s}")
            await self.db.rollback()
            return None

    async def delete_category(self, category_id: int) -> bool:
        """Delete a category by setting is_active to False"""
        try:
            # Get existing category
            category = await self.category_repo.find_by(id=category_id)
            if not category:
                self.logger.warning(f"Category with ID {category_id} not found")
                return False

            # Soft delete
            await self.category_repo.soft_delete(category)
            await self.db.commit()
            return True
        except Exception as e:
            self.logger.exception(f"Error deleting category {category_id}: {e!s}")
            await self.db.rollback()
            return False
