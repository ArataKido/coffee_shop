from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.models.order import OrderStatus


class OrderItemBase(BaseModel):
    product_id: int
    quantity: int = 1


class OrderItemCreate(OrderItemBase):
    pass


class OrderItemUpdate(BaseModel):
    quantity: Optional[int] = None


class OrderItemInDB(OrderItemBase):
    id: int
    order_id: int
    unit_price: float
    
    class Config:
        from_attributes = True


class OrderBase(BaseModel):
    user_id: int


class OrderCreate(OrderBase):
    items: List[OrderItemCreate]


class OrderUpdate(BaseModel):
    status: Optional[OrderStatus] = None


class OrderInDB(OrderBase):
    id: int
    status: OrderStatus
    total_amount: float
    created_at: datetime
    
    class Config:
        from_attributes = True


class OrderDetail(OrderInDB):
    items: List[OrderItemInDB] = []
    
    class Config:
        from_attributes = True 