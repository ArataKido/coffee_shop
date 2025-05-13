from pydantic import BaseModel, Field
from typing import Optional, List


class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    image_url: Optional[str] = None
    category_id: int


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    image_url: Optional[str] = None
    category_id: Optional[int] = None
    is_active: Optional[bool] = None


class ProductInDB(ProductBase):
    id: int
    is_active: bool
    
    class Config:
        from_attributes = True


class ProductDetail(ProductInDB):
    category_name: Optional[str] = None
    
    class Config:
        from_attributes = True 