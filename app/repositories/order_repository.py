from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.exceptions.repository_exceptions import EntityNotFoundException
from app.models.order import Order, OrderStatus
from app.models.order_item import OrderItem
from app.schemas.order_schema import OrderCreate, OrderItemCreate
from app.repositories.base_repository import BaseRepository
from app.utils.loggers.logger import Logger


class OrderRepository(BaseRepository):
    def __init__(self, db: AsyncSession, logger: Logger):
        self.logger = logger
        super().__init__(db, Order)

    async def create_order(self, order_data: OrderCreate, creator_id: int | None) -> Order:
        try:
            order = self._create_model(
                user_id=order_data.user_id,
                status=OrderStatus.PENDING,
                total_amount=0,  # Will update after adding items
            )
            order = self.add(order, created_by_user_id=creator_id)
            items = self._add_items_to_order(self, order_id=order.id, items=order_data.items)
            order.total_amount = self._count_total_price(items)
            self.db.commit()
            return order
        except EntityNotFoundException:
            self.db.rollback()
            return None
        except Exception as e:
            self.logger.exception(f"Error creating order: {e!s}")
            self.db.rollback()
            return None

    async def delete_order(self, order: Order, updater_id: int) -> None:
        try:
            order.status = OrderStatus.CANCELLED
            await self.update(order, updated_by_user_id=updater_id)
            await self.soft_delete(order, deleted_by_user_id=updater_id)
            await self.db.commit()
        except Exception as e:
            self.logger.exception(f"Error cancelling order {order.id}: {e!s}")
            await self.db.rollback()

    async def _add_items_to_order(self, order_id: int, items: list[OrderItemCreate]) -> list[OrderItem]:
        items = []
        for item_data in items:
            product = await self.product_repo.find_by_id(item_data.product_id)
            if not product or not product.is_active:
                self.logger.warning(f"Product {item_data.product_id} not found or inactive")
                raise EntityNotFoundException

            order_item = OrderItem(
                order_id=order_id,
                product_id=product.id,
                quantity=item_data.quantity,
                unit_price=product.price,
            )
            self.db.add(order_item)
            items.append(order_item)
            # Update total
        return items

    async def _count_total_price(self, items: OrderItem) -> int:
        total_amount = 0

        for item in items:
            total_amount += item.quantity * item.unit_price
        return total_amount

    async def find_with_items(self, order_id: int) -> Order | None:
        """Find an order with its items"""
        query = select(Order).where(Order.id == order_id, Order.is_active == True).options(selectinload(Order.items))  # noqa: E712
        result = await self.db.execute(query)
        return result.scalars().first()

    async def find_by_status(self, status: str) -> list[Order]:
        """Find orders by status"""
        query = select(Order).where(Order.status == status)
        result = await self.db.execute(query)
        return result.scalars().all()
