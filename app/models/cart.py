from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.cart_product import CartProduct
    from app.models.user import User


class Cart(BaseModel):
    __tablename__ = "carts"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    user: Mapped["User"] = relationship("User", back_populates="carts")
    cart_products: Mapped[list["CartProduct"]] = relationship("CartProduct", back_populates="cart")

    @property
    def subtotal(self) -> float:
        return self.quantity * self.product.price
