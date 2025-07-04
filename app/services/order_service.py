from sqlalchemy.ext.asyncio import AsyncSession
from app.models.order import OrderStatus
from app.repositories.order_repository import OrderRepository
from app.repositories.product_repository import ProductRepository
from app.schemas.order_schema import OrderCreate, OrderDetail, OrderInDB, OrderUpdate
from app.utils.tasks import send_admin_order_notification
from app.utils.loggers.logger import Logger


class OrderService:
    def __init__(
        self, db: AsyncSession, order_repository: OrderRepository, product_repository: ProductRepository, logger: Logger
    ):
        self.db = db
        self.order_repo = order_repository
        self.product_repo = product_repository
        self.logger = logger

    async def get_order_by_id(self, order_id: int) -> OrderDetail | None:
        """Get order by ID with items"""
        try:
            order = await self.order_repo.find_with_items(order_id)
            if not order:
                return None
            return OrderDetail.model_validate(order)

        except Exception as e:
            self.logger.exception(f"Error getting order by ID {order_id}: {e!s}")
            return None

    async def get_all_orders(self) -> list[OrderInDB] | None:
        """Get all orders"""
        try:
            orders = await self.order_repo.find_all()
            return [OrderInDB.model_validate(order) for order in orders]

        except Exception as e:
            self.logger.exception(f"Error getting all orders: {e!s}")
            return None

    async def get_user_orders(self, user_id: int, order_status: OrderStatus = None) -> list[OrderInDB] | None:
        """Get orders for a specific user"""
        try:
            orders = await self.order_repo.find_all_by(user_id=user_id, status=order_status)
            return [OrderInDB.model_validate(order) for order in orders]

        except Exception as e:
            self.logger.exception(f"Error getting orders for user {user_id}: {e!s}")
            return None

    async def create_order(self, order_data: OrderCreate, creator_id: int | None = None) -> OrderDetail | None:
        """Create a new order with items"""
        try:
            order = self.order_repo.create_order(order_data=order_data, creator_id=creator_id)
            # Calculate total and validate products
            send_admin_order_notification.apply_async(args=[order.user_id, order.id])
            # Get complete order with items
            return await self.get_order_by_id(order.id)

        except Exception as e:
            self.logger.exception(f"Error creating order: {e!s}")
            return None

    async def update_order_status(
        self, order_id: int, order_data: OrderUpdate, updater_id: int | None = None
    ) -> OrderInDB | None:
        """Update order status"""
        try:
            # Get existing order
            order = await self.order_repo.find_by_id(order_id)
            if not order:
                self.logger.warning(f"Order with ID {order_id} not found")
                return None

            # Update status if provided
            if order_data.status is not None:
                order.status = order_data.status

            # Update in database
            await self.order_repo.update_and_commit(order, updated_by_user_id=updater_id)
            return OrderInDB.model_validate(order)

        except Exception as e:
            self.logger.exception(f"Error updating order {order_id}: {e!s}")
            return None

    async def delete_order(self, order_id: int, updater_id: int | None = None) -> bool:
        """Cancel an order by setting status to CANCELLED"""
        try:
            # Get existing order
            order = await self.order_repo.find_by_id(order_id)
            if not order:
                self.logger.warning(f"Order with ID {order_id} not found")
                return False

            # Only allow cancellation for pending or processing orders
            if order.status not in [OrderStatus.PENDING, OrderStatus.PROCESSING]:
                self.logger.warning(f"Cannot cancel order {order_id} with status {order.status}")
                return False

            self.order_repo.delete_order(order=order, updater_id=updater_id)
            return True

        except Exception as e:
            self.logger.exception(f"Error cancelling order {order_id}: {e!s}")
            return False
