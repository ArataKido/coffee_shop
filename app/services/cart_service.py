from app.repositories.cart_repository import CartRepository
from app.repositories.product_repository import ProductRepository
from app.schemas.cart_schema import CartDetail, CartProductCreate, CartItemUpdate
from app.utils.loggers.logger import Logger


class CartService:
    def __init__(self, cart_repository: CartRepository, product_repository: ProductRepository, logger: Logger):
        self.cart_repo = cart_repository
        self.product_repo = product_repository
        self.logger = logger

    async def get_user_cart(self, user_id: int) -> CartDetail | None:
        """Get cart for a user"""
        try:
            # Get cart items with products
            cart = await self.cart_repo.find_by_user_id_detail(user_id=user_id)
            return CartDetail.model_validate(cart)

        except Exception as e:
            self.logger.exception(f"Error getting cart for user {user_id}: {e!s}")
            return None

    async def add_product_to_cart(self, user_id: int, product_data: CartProductCreate) -> CartDetail | None:
        """Add an item to the cart"""
        try:
            product = await self.product_repo.find_by(id=product_data.product_id, is_active=True)
            if not product or not product.is_active:
                self.logger.warning(f"Product {product_data.product_id} not found or inactive")
                return None

            cart = await self.cart_repo.find_by(user_id=user_id)
            if not cart:
                await self.cart_repo.create_cart()

            await self.cart_repo.add_product_to_cart(cart_id=cart.id, user_id=user_id, product_data=product_data)
            return await self.get_user_cart(user_id)

        except Exception as e:
            self.logger.exception(f"Error adding item to cart for user {user_id}: {e!s}")
            return None

    async def update_cart_product(
        self, user_id: int, product_id: int, product_data: CartItemUpdate
    ) -> CartDetail | None:
        """Update a cart item"""
        try:
            # Get cart item
            cart_product = await self.cart_repo.find_product_in_cart(user_id, product_id)
            if not cart_product:
                self.logger.warning(f"Cart item {product_id} not found in user's cart")
                return None

            self.cart_repo.update_cart_product()
            return await self.get_user_cart(user_id)

        except Exception as e:
            self.logger.exception(f"Error updating cart item {product_id} for user {user_id}: {e!s}")
            return None

    async def remove_cart_product(self, user_id: int, product_id: int) -> CartDetail | None:
        """Remove an item from the cart"""
        try:
            cart_product = await self.cart_repo.find_product_in_cart(user_id=user_id, product_id=product_id)
            self.logger.error(cart_product)
            if not cart_product:
                self.logger.warning(f"Cart item {product_id} not found in user's cart")
                return None

            # Remove item
            await self.cart_repo.delete_product_from_cart(
                cart_id=cart_product.cart_id, product_id=cart_product.product_id
            )
            return await self.get_user_cart(user_id)

        except Exception as e:
            self.logger.exception(f"Error removing cart item {product_id} for user {user_id}: {e!s}")
            return None

    async def clear_cart(self, user_id: int) -> bool:
        """Clear all items from the cart"""
        try:
            await self.cart_repo.clear_cart(user_id=user_id)
            return True

        except Exception as e:
            self.logger.exception(f"Error clearing cart for user {user_id}: {e!s}")
            return False
