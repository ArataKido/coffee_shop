from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Dict, Any
import logging

from app.repositories.order_repository import OrderRepository
from app.repositories.product_repository import ProductRepository
from app.schemas.order import OrderCreate, OrderUpdate, OrderInDB, OrderDetail
from app.models.order import OrderStatus
from app.models.order_item import OrderItem

logger = logging.getLogger(__name__)

class OrderService:
    def __init__(self, db: AsyncSession, order_repository:OrderRepository, product_repository:ProductRepository):
        self.db = db
        self.order_repo = order_repository
        self.product_repo = product_repository
    
    async def get_order_by_id(self, order_id: int) -> Optional[OrderDetail]:
        """Get order by ID with items"""
        try:
            order = await self.order_repo.find_with_items(order_id)
            if not order:
                return None
                
            return OrderDetail.model_validate(order)
        except Exception as e:
            logger.error(f"Error getting order by ID {order_id}: {str(e)}")
            return None
    
    async def get_all_orders(self) -> List[OrderInDB]:
        """Get all orders"""
        try:
            orders = await self.order_repo.find_all()
            return [OrderInDB.model_validate(order) for order in orders]
        except Exception as e:
            logger.error(f"Error getting all orders: {str(e)}")
            return []
    
    async def get_user_orders(self, user_id: int, order_status: OrderStatus = None) -> List[OrderInDB]:
        """Get orders for a specific user"""
        try:
            orders = await self.order_repo.find_by_user(user_id, order_status)
            return [OrderInDB.model_validate(order) for order in orders]
        except Exception as e:
            logger.error(f"Error getting orders for user {user_id}: {str(e)}")
            return []
    
    async def create_order(self, order_data: OrderCreate, creator_id: Optional[int] = None) -> Optional[OrderDetail]:
        """Create a new order with items"""
        try:
            # Calculate total and validate products
            total_amount = 0
            order_items = []
            
            # Create order
            order = self.order_repo.create_model(
                user_id=order_data.user_id,
                status=OrderStatus.PENDING,
                total_amount=0  # Will update after adding items
            )
            
            # Save to database to get ID
            created_order = await self.order_repo.add(order, created_by_user_id=creator_id)
            
            # Create order items
            for item_data in order_data.items:
                product = await self.product_repo.find_by_id(item_data.product_id)
                if not product or not product.is_active:
                    logger.warning(f"Product {item_data.product_id} not found or inactive")
                    await self.db.rollback()
                    return None
                
                # Create order item
                order_item = OrderItem(
                    order_id=created_order.id,
                    product_id=product.id,
                    quantity=item_data.quantity,
                    unit_price=product.price
                )
                
                # Add to DB
                self.db.add(order_item)
                order_items.append(order_item)
                
                # Update total
                total_amount += order_item.quantity * product.price
            
            # Update order total
            created_order.total_amount = total_amount
            
            # Commit transaction
            await self.db.commit()
            
            # Get complete order with items
            return await self.get_order_by_id(created_order.id)
        except Exception as e:
            logger.error(f"Error creating order: {str(e)}")
            await self.db.rollback()
            return None
    
    async def update_order_status(self, order_id: int, order_data: OrderUpdate, updater_id: Optional[int] = None) -> Optional[OrderInDB]:
        """Update order status"""
        try:
            # Get existing order
            order = await self.order_repo.find_by_id(order_id)
            if not order:
                logger.warning(f"Order with ID {order_id} not found")
                return None
            
            # Update status if provided
            if order_data.status is not None:
                order.status = order_data.status
                
            # Update in database
            await self.order_repo.update(
                order, 
                updated_by_user_id=updater_id
            )
            await self.db.commit()
            return OrderInDB.model_validate(order)
        except Exception as e:
            logger.error(f"Error updating order {order_id}: {str(e)}")
            await self.db.rollback()
            return None
    
    async def cancel_order(self, order_id: int, updater_id: Optional[int] = None) -> bool:
        """Cancel an order by setting status to CANCELLED"""
        try:
            # Get existing order
            order = await self.order_repo.find_by_id(order_id)
            if not order:
                logger.warning(f"Order with ID {order_id} not found")
                return False
            
            # Only allow cancellation for pending or processing orders
            if order.status not in [OrderStatus.PENDING, OrderStatus.PROCESSING]:
                logger.warning(f"Cannot cancel order {order_id} with status {order.status}")
                return False
            
            # Set status to CANCELLED
            order.status = OrderStatus.CANCELLED
            
            # Update in database
            await self.order_repo.update(
                order, 
                updated_by_user_id=updater_id
            )
            await self.db.commit()
            return True
        except Exception as e:
            logger.error(f"Error cancelling order {order_id}: {str(e)}")
            await self.db.rollback()
            return False 