from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.models.product import Product
from app.schemas.product_schema import ProductUpdate
from app.repositories.base_repository import BaseRepository


class ProductRepository(BaseRepository):
    def __init__(self, db: AsyncSession):
        super().__init__(db, Product)

    async def find_by_category(self, category_id: int, limit: int = None, offset: int = None) -> list[Product]:
        """Find products by category ID"""
        query = select(Product).where(Product.category_id == category_id, Product.is_active == True)
        if limit is not None:
            query = query.limit(limit)

        if offset is not None:
            query = query.offset(offset)

        result = await self.db.execute(query)
        return result.scalars().all()

    async def find_with_category(self, product_id: int) -> Product | None:
        """Find a product with its category"""
        query = (
            select(Product)
            .where(Product.id == product_id, Product.is_active == True)
            .options(joinedload(Product.category))
        )
        result = await self.db.execute(query)
        return result.scalars().first()

    async def update_product(self, product_update:ProductUpdate, product:Product, updater_id:int) -> Product | None:
        try:
            # Update fields if provided
            for field in  ["name", "description", "price", "image_url", "category_id", "is_active"]:
                value = getattr(product_update, field)
                if value is not None:
                    setattr(product, field, value)
            # Update in database
            await self.update_and_commit(product, updated_by_user_id=updater_id)
            return product
        except Exception:
            await self.db.rollback()
            self.logger.exception(f"Error updating product {product.id}")
            return None
    async def search_by_name(self, search_term: str) -> list[Product]:
        """Search products by name"""
        query = select(Product).where(Product.name.ilike(f"%{search_term}%"), Product.is_active == True)
        result = await self.db.execute(query)
        return result.scalars().all()
