from pydantic import BaseModel
from typing import Optional, List


class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class CategoryInDB(CategoryBase):
    id: int
    is_active: bool
    
    class Config:
        from_attributes = True 