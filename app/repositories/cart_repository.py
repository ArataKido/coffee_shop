from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.cart import Cart
from app.models.cart_product import CartProduct
from app.repositories.base_repository import BaseRepository


class CartRepository(BaseRepository):
    def __init__(self, db: AsyncSession):
        super().__init__(db, Cart)

    async def find_product_in_cart(self, user_id: int, product_id: int) -> CartProduct | None:
        """Find item in users cart"""
        query = select(CartProduct).where(
            CartProduct.cart.has(Cart.user_id == user_id), CartProduct.product_id == product_id
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def find_by_user_id_detail(self, user_id: int) -> Cart | None:
        """Find user's cart items with product details"""
        query = (
            select(Cart)
            .where(Cart.user_id == user_id)
            .options(selectinload(Cart.cart_products).joinedload(CartProduct.product))
        )
        result = await self.db.execute(query)
        return result.scalars().first()

    async def delete_product_from_cart(self, cart_id: int, product_id: int) -> None:
        query = delete(CartProduct).where(CartProduct.cart_id == cart_id, CartProduct.product_id == product_id)
        await self.db.execute(query)

    async def clear_cart(self, user_id: int) -> None:
        query = delete(CartProduct).where(CartProduct.cart.has(Cart.user_id == user_id))
        await self.db.execute(query)
