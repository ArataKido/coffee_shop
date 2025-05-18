from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.order import Order
from app.repositories.base_repository import BaseRepository


class OrderRepository(BaseRepository):
    def __init__(self, db: AsyncSession):
        super().__init__(db, Order)

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
