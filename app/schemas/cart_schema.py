from pydantic import BaseModel

from app.schemas.product_schema import ProductInDB


class CartBase(BaseModel):
    product_id: int
    quantity: int = 1


class CartProductCreate(CartBase):
    pass


class CartItemUpdate(BaseModel):
    quantity: int | None = None


class CartProductBase(BaseModel):
    quantity: int
    product: ProductInDB

    class Config:
        from_attributes = True


class CartDetail(BaseModel):
    id: int
    cart_products: list[CartProductBase] = []

    class Config:
        from_attributes = True
