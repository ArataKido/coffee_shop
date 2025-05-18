from pydantic import BaseModel


class ProductBase(BaseModel):
    name: str
    description: str | None = None
    price: float
    image_url: str | None = None
    category_id: int


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    image_url: str | None = None
    category_id: int | None = None
    is_active: bool | None = None


class ProductInDB(ProductBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True


class ProductDetail(ProductInDB):
    category_name: str | None = None

    class Config:
        from_attributes = True
