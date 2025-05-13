from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List, TYPE_CHECKING

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.product import Product


class Category(BaseModel):
    __tablename__ = "categories"

    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    # Relationships
    products: Mapped[List["Product"]] = relationship(back_populates="category", cascade="all, delete-orphan")