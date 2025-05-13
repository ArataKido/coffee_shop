from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.schemas.cart import CartDetail, CartItemCreate, CartItemUpdate
from app.services.cart_service import CartService
from app.dependencies import get_cart_service
from app.db import get_db

router = APIRouter(
    prefix="/cart",
    tags=["cart"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{user_id}", response_model=CartDetail)
async def read_user_cart(
    user_id: int,
    cart_service: CartService = Depends(get_cart_service)
):
    """Get a user's cart with items"""
    cart = await cart_service.get_user_cart(user_id)
    if not cart:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error getting cart"
        )
    return cart


@router.post("/{user_id}/items", response_model=CartDetail)
async def add_item_to_cart(
    user_id: int,
    item: CartItemCreate,
    cart_service: CartService = Depends(get_cart_service)
):
    """Add an item to the cart"""
    cart = await cart_service.add_item_to_cart(user_id, item)
    if not cart:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not add item to cart, check product exists"
        )
    return cart


@router.patch("/{user_id}/items/{item_id}", response_model=CartDetail)
async def update_cart_item(
    user_id: int,
    item_id: int,
    item_data: CartItemUpdate,
    cart_service: CartService = Depends(get_cart_service)
):
    """Update a cart item quantity"""
    cart = await cart_service.update_cart_item(user_id, item_id, item_data)
    if not cart:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart item not found"
        )
    return cart


@router.delete("/{user_id}/items/{item_id}", response_model=CartDetail)
async def remove_cart_item(
    user_id: int,
    item_id: int,
    cart_service: CartService = Depends(get_cart_service)
):
    """Remove an item from the cart"""
    cart = await cart_service.remove_cart_item(user_id, item_id)
    if not cart:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart item not found"
        )
    return cart


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def clear_cart(
    user_id: int,
    cart_service: CartService = Depends(get_cart_service)
):
    """Clear all items from the cart"""
    success = await cart_service.clear_cart(user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error clearing cart"
        )
    return 