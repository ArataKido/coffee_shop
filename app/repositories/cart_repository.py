from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.cart import Cart
from app.models.cart_product import CartProduct
from app.repositories.base_repository import BaseRepository
from app.schemas.cart_schema import CartProductCreate


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

    async def create_cart(self, user_id:int) -> None:
        cart = self.cart_repo.create_model(user_id=user_id)
        await self.cart_repo.add_and_commit(cart)

    async def add_product_to_cart(self, cart_id:int, user_id:int, product_data:CartProductCreate):
        try:
            cart_product = await self.find_product_in_cart(
                user_id=user_id, product_id=product_data.product_id
                )
            if cart_product:
                # Update quantity
                cart_product.quantity += product_data.quantity
                await self.db.commit()
            else:
                # Create new cart item
                cart_item = CartProduct(
                    cart_id=cart_id, product_id=product_data.product_id, quantity=product_data.quantity
                )
                self.db.add(cart_item)
                await self.db.commit()
        except Exception as e:
            self.logger.exception(f"Error adding item to cart for user {user_id}: {e!s}")
            await self.db.rollback()

    async def delete_product_from_cart(self, cart_id: int, product_id: int) -> None:
        query = delete(CartProduct).where(CartProduct.cart_id == cart_id, CartProduct.product_id == product_id)
        await self.db.execute(query)

    async def clear_cart(self, user_id: int) -> None:
        query = delete(CartProduct).where(CartProduct.cart.has(Cart.user_id == user_id))
        await self.db.execute(query)
