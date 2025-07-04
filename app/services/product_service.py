from app.repositories.category_repository import CategoryRepository
from app.repositories.product_repository import ProductRepository
from app.schemas.product_schema import ProductCreate, ProductDetail, ProductInDB, ProductUpdate
from app.utils.loggers.logger import Logger


class ProductService:
    def __init__(
        self,
        product_repository: ProductRepository,
        category_repository: CategoryRepository,
        logger: Logger,
    ):
        self.product_repo = product_repository
        self.category_repo = category_repository
        self.logger = logger

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
        except Exception:
            self.logger.exception(f"Error getting product by ID {product_id}")
            return None

    async def get_all_products(self) -> list[ProductInDB] | None:
        """Get all products"""
        try:
            products = await self.product_repo.get_all()
            return [ProductInDB.model_validate(product) for product in products]
        except Exception:
            self.logger.exception("Error getting all products")
            return None

    async def get_products_by_category(
        self, category_id: int, limit: int | None = None, offset: int | None = None
    ) -> list[ProductInDB] | None:
        """Get products by category ID"""
        try:
            products = await self.product_repo.find_by_category(category_id, limit, offset)
            return [ProductInDB.model_validate(product) for product in products]
        except Exception:
            self.logger.exception(f"Error getting products by category {category_id}")
            return None

    async def create_product(self, product_data: ProductCreate, creator_id: int | None = None) -> ProductInDB | None:
        """Create a new product"""
        try:
            # Check if category exists
            category = await self.category_repo.find_by_id(product_data.category_id)
            if not category or not category.is_active:
                self.logger.warning(f"Category with ID {product_data.category_id} not found or inactive")
                return None

            # Create product
            product = self.product_repo._create_model(
                name=product_data.name,
                description=product_data.description,
                price=product_data.price,
                image_url=product_data.image_url,
                category_id=product_data.category_id,
            )
            # Save to database
            created_product = await self.product_repo.add_and_commit(product, created_by_user_id=creator_id)
            return ProductInDB.model_validate(created_product)
        except Exception:
            self.logger.exception("Error creating product")
            await self.db.rollback()
            return None

    async def update_product(
        self, product_id: int, product_data: ProductUpdate, updater_id: int | None = None
    ) -> ProductInDB | None:
        """Update a product"""
        try:
            product = await self.product_repo.find_by(id=product_id)
            if not product:
                self.logger.warning(f"Product with ID {product_id} not found")
                return None

            # Check category if updating
            if product_data.category_id is not None:
                category = await self.category_repo.find_by_id(product_data.category_id)
                if not category or not category.is_active:
                    self.logger.warning(f"Category with ID {product_data.category_id} not found or inactive")
                    return None

            product = await self.product_repo.update_product(
                product_data=product_data,
                product=product,
                updater_id=updater_id
                )
            return ProductInDB.model_validate(product)
        except Exception:
            self.logger.exception(f"Error updating product {product_id}")
            return None

    async def delete_product(self, product_id: int) -> bool:
        """Delete a product by setting is_active to False"""
        try:
            # Get existing product
            product = await self.product_repo.find_by_id(product_id)
            if not product:
                self.logger.warning(f"Product with ID {product_id} not found")
                return False
            # Soft delete
            await self.product_repo.soft_delete(product)
            return True
        except Exception:
            self.logger.exception(f"Error deleting product {product_id}")
            return False
