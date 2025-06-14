from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi_pagination import Page, paginate
from dishka.integrations.fastapi import FromDishka, DishkaRoute

from app.dependencies.auth_dependencies import user_is_admin
from app.schemas.product_schema import ProductCreate, ProductDetail, ProductInDB, ProductUpdate
from app.services.product_service import ProductService

router = APIRouter(
    prefix="/products",
    tags=["products"],
    responses={404: {"description": "Not found"}},
    route_class=DishkaRoute
)


@router.post("/", response_model=ProductInDB, status_code=status.HTTP_201_CREATED)
async def create_product(
    product: ProductCreate, product_service: FromDishka[ProductService], user=Depends(user_is_admin)
):
    """Create a new product"""
    created_product = await product_service.create_product(product)
    if not created_product:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Could not create product, check category exists"
        )
    return created_product


@router.get("/", response_model=Page[ProductInDB])
async def read_products(
    product_service: FromDishka[ProductService],
    category_id: int | None = Query(None, description="Filter by category ID"),
    limit: int | None = Query(None, description="Limit how many products you retrieve "),
    offset: int | None = Query(None),
):
    """Get all products, optionally filtered by category"""
    if category_id:
        products = await product_service.get_products_by_category(category_id, limit, offset)
    else:
        products = await product_service.get_all_products()

    return paginate(products)


@router.get("/{product_id}", response_model=ProductDetail)
async def read_product(product_id: int, product_service: FromDishka[ProductService]):
    """Get a product by ID"""
    product = await product_service.get_product_by_id(product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product


@router.patch("/{product_id}", response_model=ProductInDB)
async def update_product(
    product_id: int,
    product: ProductUpdate,
    product_service: FromDishka[ProductService],
    user=Depends(user_is_admin),
):
    """Update a product"""
    updated_product = await product_service.update_product(product_id, product)
    if not updated_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found or category invalid")
    return updated_product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: int, product_service: FromDishka[ProductService], user=Depends(user_is_admin)
):
    """Delete a product"""
    success = await product_service.delete_product(product_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
