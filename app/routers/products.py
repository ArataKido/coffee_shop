from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.schemas.product import ProductCreate, ProductUpdate, ProductInDB, ProductDetail
from app.services.product_service import ProductService
from app.dependencies import get_product_service
from app.db import get_db

router = APIRouter(
    prefix="/products",
    tags=["products"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=ProductInDB, status_code=status.HTTP_201_CREATED)
async def create_product(
    product: ProductCreate,
    product_service: ProductService = Depends(get_product_service)
):
    """Create a new product"""
    created_product = await product_service.create_product(product)
    if not created_product:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not create product, check category exists"
        )
    return created_product


@router.get("/", response_model=List[ProductInDB])
async def read_products(
    category_id: Optional[int] = Query(None, description="Filter by category ID"),
    limit: Optional[int] = Query(None, description="Limit how many products you retrieve "),
    offset: Optional[int] = Query(None),
    product_service: ProductService = Depends(get_product_service)
):
    """Get all products, optionally filtered by category"""
    
    if category_id:
        products = await product_service.get_products_by_category(category_id, limit, offset)
    else:
        products = await product_service.get_all_products()
        
    return products


@router.get("/{product_id}", response_model=ProductDetail)
async def read_product(
    product_id: int,
    product_service: ProductService = Depends(get_product_service)
):
    """Get a product by ID"""
    product = await product_service.get_product_by_id(product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return product


@router.patch("/{product_id}", response_model=ProductInDB)
async def update_product(
    product_id: int,
    product: ProductUpdate,
    product_service: ProductService = Depends(get_product_service)
):
    """Update a product"""
    updated_product = await product_service.update_product(product_id, product)
    if not updated_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found or category invalid"
        )
    return updated_product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: int,
    product_service: ProductService = Depends(get_product_service)
):
    """Delete a product"""
    success = await product_service.delete_product(product_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return 