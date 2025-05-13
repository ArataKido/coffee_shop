from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, Optional, TYPE_CHECKING

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.order import Order
    from app.models.cart import Cart


class User(BaseModel):
    __tablename__ = "users"

    username: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Relationships
    orders: Mapped[List["Order"]] = relationship(back_populates="user")
    carts: Mapped[List["Cart"]] = relationship(back_populates="user", cascade="all, delete-orphan")

