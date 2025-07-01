from datetime import datetime

from pydantic import BaseModel

from app.models.order import OrderStatus


class OrderItemBase(BaseModel):
    product_id: int
    quantity: int = 1


class OrderItemCreate(OrderItemBase):
    pass


class OrderItemUpdate(BaseModel):
    quantity: int | None = None


class OrderItemInDB(OrderItemBase):
    id: int
    order_id: int
    unit_price: float

    class Config:
        from_attributes = True



class OrderCreate(BaseModel):
    items: list[OrderItemCreate]


class OrderUpdate(BaseModel):
    status: OrderStatus | None = None


class OrderInDB(BaseModel):
    id: int
    user_id:int
    status: OrderStatus
    total_amount: float
    created_at: datetime

    class Config:
        from_attributes = True


class OrderDetail(OrderInDB):
    items: list[OrderItemInDB] = []

    class Config:
        from_attributes = True
