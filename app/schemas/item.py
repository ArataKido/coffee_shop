from pydantic import BaseModel
from typing import Optional
from .category import Category  # Forward reference if needed

class ItemBaseSchema(BaseModel):
    name: str
    price: float

class ItemCreateSchema(ItemBaseSchema):
    category_id: int

class ItemUpdateSchema(ItemBaseSchema):
    name: Optional[str] = None
    price: Optional[float] = None
    category_id: Optional[int] = None

class ItemSchema(ItemBaseSchema):
    id: int
    category: Optional[Category] = None  # Reference to the category
    
    class Config:
        orm_mode = True  # For Pydantic v1. Use `from_attributes = True` for v2 