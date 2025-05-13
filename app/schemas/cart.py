from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime
from app.schemas.product import ProductInDB


class CartBase(BaseModel):
    product_id: int
    quantity: int = 1

class CartItemCreate(CartBase):
    pass

class CartItemUpdate(BaseModel):
    quantity: Optional[int] = None

class CartProductBase(BaseModel):
    quantity:int
    product: ProductInDB 
    
    class Config:
        from_attributes = True

class CartDetail(BaseModel):
    id: int
    user_id: int
    cart_products: List[CartProductBase] = []
    
    class Config:
        from_attributes = True




