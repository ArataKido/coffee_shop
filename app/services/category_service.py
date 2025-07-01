from app.repositories.category_repository import CategoryRepository
from app.schemas.category_schema import CategoryCreate, CategoryInDB, CategoryUpdate
from app.utils.loggers.logger import Logger


class CategoryService:
    def __init__(self, category_repository: CategoryRepository, logger: Logger):
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

    async def get_all_categories(self) -> list[CategoryInDB] | None:
        """Get all categories"""
        try:
            categories = await self.category_repo.get_all()
            return [CategoryInDB.model_validate(cat) for cat in categories]

        except Exception as e:
            self.logger.exception(f"Error getting all categories: {e!s}")
            return None

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
            category = self.category_repo.create_category(category_data, creator_id)
            return CategoryInDB.model_validate(category)

        except Exception as e:
            self.logger.exception(f"Error creating category: {e!s}")
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

            category = await self.category_repo.update_category(
                category=category, category_update=category_data, updater_id=updater_id
            )
            return CategoryInDB.model_validate(category)

        except Exception as e:
            self.logger.exception(f"Error updating category {category_id}: {e!s}")
            return None

    async def delete_category(self, category_id: int) -> bool:
        """Delete a category by setting is_active to False"""
        try:
            # Get existing category
            category = await self.category_repo.find_by(id=category_id)
            if not category:
                self.logger.warning(f"Category with ID {category_id} not found")
                return False

            await self.category_repo.soft_delete(category)
            return True

        except Exception as e:
            self.logger.exception(f"Error deleting category {category_id}: {e!s}")
            return False
