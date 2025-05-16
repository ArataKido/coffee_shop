from sqlalchemy.ext.asyncio import AsyncSession
import logging

from app.exceptions.exceptions import NotFoundException
from app.repositories.cart_repository import CartRepository
from app.repositories.product_repository import ProductRepository
from app.schemas.cart import CartDetail, CartItemCreate, CartItemUpdate
from app.models.cart_product import CartProduct

logger = logging.getLogger(__name__)

class CartService:
    def __init__(self, db: AsyncSession, cart_repository: CartRepository, product_repository:ProductRepository):
        self.db = db
        self.cart_repo = cart_repository
        self.product_repo = product_repository
    
    async def get_user_cart(self, user_id: int) -> CartDetail | None:
        """Get cart for a user"""
        # Get cart items with products
        cart = await self.cart_repo.find_by_user_id_detail(user_id=user_id)
        if not cart:
            logger.error(f"Error getting cart for user {user_id}: {str(e)}")
            raise NotFoundException("Users cart was not found")
        return CartDetail.model_validate(cart)
    
    async def add_item_to_cart(self, user_id: int, item_data: CartItemCreate) -> CartDetail | None:
        """Add an item to the cart"""
        try:
        # Check if product exists and is active
            product = await self.product_repo.find_by(id=item_data.product_id, is_active=True)
            if not product or not product.is_active:
                logger.warning(f"Product {item_data.product_id} not found or inactive")
                return None

            # Check if item already in cart
            cart = await self.cart_repo.find_by(user_id=user_id)
            if not cart:
                cart = self.cart_repo.create_model(user_id=user_id)
                await self.cart_repo.add_and_commit(cart)

            cart_product = await self.cart_repo.find_product_in_cart(user_id=user_id, product_id=item_data.product_id)
            if cart_product:
                # Update quantity
                cart_product.quantity += item_data.quantity
                await self.db.commit()
            else:
                # Create new cart item
                cart_item = CartProduct(
                    cart_id=cart.id,
                    product_id=item_data.product_id,
                    quantity=item_data.quantity
                )
                self.db.add(cart_item)
                await self.db.commit()
                # Return updated cart
            return await self.get_user_cart(user_id)
        except Exception as e:
            logger.error(f"Error adding item to cart for user {user_id}: {str(e)}")
            await self.db.rollback()
            return None
    
    async def update_cart_item(self, user_id: int, product_id: int, item_data: CartItemUpdate) -> CartDetail | None:
        """Update a cart item"""
        try:
            # Get cart item
            cart_product = await self.cart_repo.find_product_in_cart(user_id, product_id)
            if not cart_product:
                logger.warning(f"Cart item {product_id} not found in user's cart")
                return None
            
            # Update quantity
            if item_data.quantity <= 0:
                # Remove item if quantity is zero or negative
                await self.cart_repo.delete_product_from_cart(cart_id=cart_product.cart_id, product_id=product_id)
                await self.db.commit()
            else:
                # Update quantity
                cart_product.quantity = item_data.quantity
                await self.db.commit()
            
            
            # Return updated cart
            return await self.get_user_cart(user_id)
        except Exception as e:
            logger.error(f"Error updating cart item {product_id} for user {user_id}: {str(e)}")
            await self.db.rollback()
            return None
    
    async def remove_cart_item(self, user_id: int, item_id: int) -> CartDetail | None:
        """Remove an item from the cart"""
        try:
            # Get cart item
            cart_item = await self.cart_repo.find_by_id(item_id)
            if not cart_item or cart_item.user_id != user_id:
                logger.warning(f"Cart item {item_id} not found in user's cart")
                return None
            
            # Remove item
            await self.cart_repo.delete(cart_item)
            await self.db.commit()
            
            # Return updated cart
            return await self.get_user_cart(user_id)
        except Exception as e:
            logger.error(f"Error removing cart item {item_id} for user {user_id}: {str(e)}")
            await self.db.rollback()
            return None
    
    async def clear_cart(self, user_id: int) -> bool:
        """Clear all items from the cart"""
        try:
            # Get cart items
            cart_items = await self.cart_repo.find_by(user_id=user_id)
            # Remove all items
            for item in cart_items:
                await self.cart_repo.permanent_delete(item)
            
            await self.db.commit()
            return True
        except Exception as e:
            logger.error(f"Error clearing cart for user {user_id}: {str(e)}")
            await self.db.rollback()
            return False 