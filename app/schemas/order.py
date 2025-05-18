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


class OrderBase(BaseModel):
    user_id: int


class OrderCreate(OrderBase):
    items: list[OrderItemCreate]


class OrderUpdate(BaseModel):
    status: OrderStatus | None = None


class OrderInDB(OrderBase):
    id: int
    status: OrderStatus
    total_amount: float
    created_at: datetime

    class Config:
        from_attributes = True


class OrderDetail(OrderInDB):
    items: list[OrderItemInDB] = []

    class Config:
        from_attributes = True
