from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import List, Optional

from app.models.order import Order, OrderStatus
from app.repositories.base_repository import BaseRepository


class OrderRepository(BaseRepository):
    def __init__(self, db: AsyncSession):
        super().__init__(db, Order)
    
    async def find_by_user(self, user_id: int, order_status: OrderStatus = None) -> List[Order]:
        """Find orders by user ID"""
        query = select(Order).where(Order.user_id == user_id)
        
        if order_status is not None: 
            query = query.filter(Order.status == order_status)
            
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def find_with_items(self, order_id: int) -> Optional[Order]:
        """Find an order with its items"""
        query = select(Order).where(
            Order.id == order_id
        ).options(
            selectinload(Order.items)
        )
        result = await self.db.execute(query)
        return result.scalars().first()
        
    async def find_by_status(self, status: str) -> List[Order]:
        """Find orders by status"""
        query = select(Order).where(Order.status == status)
        result = await self.db.execute(query)
        return result.scalars().all() 