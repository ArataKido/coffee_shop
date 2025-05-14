from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.orm import joinedload, selectinload
from typing import List, Optional

from app.models.cart import Cart
from app.models.cart_product import CartProduct
from app.repositories.base_repository import BaseRepository


class CartRepository(BaseRepository):
    def __init__(self, db: AsyncSession):
        super().__init__(db, Cart)

    async def find_product_in_cart(self, user_id: int, product_id: int) -> Optional[Cart]:
        """Find item in users cart """
        query = select(Cart).where(
            Cart.user_id == user_id,
            CartProduct.product_id == product_id
        ).options(
            joinedload(Cart.cart_products)
        )
        result = await self.db.execute(query)
        return result.scalars().first()
        
    
    async def find_by_user_id_detail(self, user_id: int) -> Optional[Cart]:
        """Find user's cart items with product details"""
        query = select(Cart).where(
            Cart.user_id == user_id
        ).options(
            selectinload(Cart.cart_products)
            .selectinload(CartProduct.product)
        )
        result = await self.db.execute(query)
        return result.scalars().first() 

    async def delete_product_from_cart(self, cart_id:int, product_id:int) -> None:
        query = delete(CartProduct).where(CartProduct.cart_id == cart_id, CartProduct.product_id == product_id)
        await self.db.execute(query)
        await self.db.commit()

