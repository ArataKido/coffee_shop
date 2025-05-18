from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.category_repository import CategoryRepository
from app.repositories.product_repository import ProductRepository
from app.schemas.product import ProductCreate, ProductDetail, ProductInDB, ProductUpdate
from app.utils.loggers.logger import Logger

logger = Logger()


class ProductService:
    def __init__(
        self, db: AsyncSession, product_repository: ProductRepository, category_repository: CategoryRepository
    ):
        self.db = db
        self.product_repo = product_repository
        self.category_repo = category_repository

    async def get_product_by_id(self, product_id: int) -> ProductDetail | None:
        """Get product by ID with category details"""
        try:
            product = await self.product_repo.find_with_category(product_id)
            if not product:
                return None

            product_data = ProductInDB.model_validate(product)
            product_detail = ProductDetail(**product_data.model_dump())
            product_detail.category_name = product.category.name if product.category else None

            return product_detail
        except Exception as e:
            logger.exception(f"Error getting product by ID {product_id}: {e!s}")
            return None

    async def get_all_products(self) -> list[ProductInDB]:
        """Get all products"""
        try:
            products = await self.product_repo.get_all()
            return [ProductInDB.model_validate(product) for product in products]
        except Exception as e:
            logger.exception(f"Error getting all products: {e!s}")
            return []

    async def get_products_by_category(
        self, category_id: int, limit: int | None = None, offset: int | None= None
    ) -> list[ProductInDB]:
        """Get products by category ID"""
        try:
            products = await self.product_repo.find_by_category(category_id, limit, offset)
            return [ProductInDB.model_validate(product) for product in products]
        except Exception as e:
            logger.exception(f"Error getting products by category {category_id}: {e!s}")
            return []

    async def create_product(self, product_data: ProductCreate, creator_id: int | None = None) -> ProductInDB | None:
        """Create a new product"""
        try:
            # Check if category exists
            category = await self.category_repo.find_by_id(product_data.category_id)
            if not category or not category.is_active:
                logger.warning(f"Category with ID {product_data.category_id} not found or inactive")
                return None

            # Create product
            product = self.product_repo.create_model(
                name=product_data.name,
                description=product_data.description,
                price=product_data.price,
                image_url=product_data.image_url,
                category_id=product_data.category_id,
            )

            # Save to database
            created_product = await self.product_repo.add_and_commit(product, created_by_user_id=creator_id)
            return ProductInDB.model_validate(created_product)
        except Exception as e:
            logger.exception(f"Error creating product: {e!s}")
            await self.db.rollback()
            return None

    async def update_product(
        self, product_id: int, product_data: ProductUpdate, updater_id: int | None = None
    ) -> ProductInDB | None:
        """Update a product"""
        try:
            # Get existing product
            product = await self.product_repo.find_by_id(product_id)
            if not product:
                logger.warning(f"Product with ID {product_id} not found")
                return None

            # Check category if updating
            if product_data.category_id is not None:
                category = await self.category_repo.find_by_id(product_data.category_id)
                if not category or not category.is_active:
                    logger.warning(f"Category with ID {product_data.category_id} not found or inactive")
                    return None

            # Update fields if provided
            if product_data.name is not None:
                product.name = product_data.name
            if product_data.description is not None:
                product.description = product_data.description
            if product_data.price is not None:
                product.price = product_data.price
            if product_data.image_url is not None:
                product.image_url = product_data.image_url
            if product_data.category_id is not None:
                product.category_id = product_data.category_id
            if product_data.is_active is not None:
                product.is_active = product_data.is_active

            # Update in database
            await self.product_repo.update(product, updated_by_user_id=updater_id)
            await self.db.commit()
            return ProductInDB.model_validate(product)
        except Exception as e:
            logger.exception(f"Error updating product {product_id}: {e!s}")
            await self.db.rollback()
            return None

    async def delete_product(self, product_id: int) -> bool:
        """Delete a product by setting is_active to False"""
        try:
            # Get existing product
            product = await self.product_repo.find_by_id(product_id)
            if not product:
                logger.warning(f"Product with ID {product_id} not found")
                return False

            # Soft delete
            await self.product_repo.soft_delete(product)
            await self.db.commit()
            return True
        except Exception as e:
            logger.exception(f"Error deleting product {product_id}: {e!s}")
            await self.db.rollback()
            return False
