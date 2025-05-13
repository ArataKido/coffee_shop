from sqlalchemy import String, ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List, TYPE_CHECKING

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.category import Category
    from app.models.order_item import OrderItem
    from app.models.cart_product import CartProduct


class Product(BaseModel):
    __tablename__ = "products"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    image_url: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), nullable=False)
    
    # Relationships
    category: Mapped["Category"] = relationship(back_populates="products")
    order_items: Mapped[List["OrderItem"]] = relationship(back_populates="product")
    cart_products: Mapped[List["CartProduct"]] = relationship(back_populates="product")

