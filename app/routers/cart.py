from fastapi import APIRouter, Depends, HTTPException, status
from dishka.integrations.fastapi import FromDishka, DishkaRoute

from app.dependencies.auth_dependencies import get_current_active_user
from app.schemas.cart_schema import CartDetail, CartProductCreate, CartItemUpdate
from app.services.cart_service import CartService
from app.schemas.user_schema import UserSchema

router = APIRouter(
    prefix="/cart",
    tags=["cart"],
    responses={404: {"description": "Not found"}},
    route_class=DishkaRoute
)


@router.get("/", response_model=CartDetail)
async def read_user_cart(cart_service: FromDishka[CartService], user=Depends(get_current_active_user)):
    """
    Get a user's cart with items

    Parameters
    ----------
        - user: current users information. used for fetching cart data
        - cart_service: Cart service used for getting cart information

    Returns
    -------
        A JSON response containing the cart information.

    """
    cart = await cart_service.get_user_cart(user.id)
    if not cart:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error getting cart")
    return cart


@router.post("/", response_model=CartDetail)
async def add_product_to_cart(
    item: CartProductCreate,
    cart_service: FromDishka[CartService],
    user: UserSchema = Depends(get_current_active_user),
):
    """
    Add item to users cart

    Parameters
    ----------
        - user_id: users id, used for fetching and adding items to the cart
        - cart_service: Cart service used for getting cart information

    Returns
    -------
        A JSON response containing the cart information.

    """
    cart = await cart_service.add_product_to_cart(user.id, item)
    if not cart:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Could not add item to cart, check product exists"
        )
    return cart


@router.patch("/{product_id}", response_model=CartDetail)
async def update_cart_product(
    product_id: int,
    item_data: CartItemUpdate,
    cart_service: FromDishka[CartService],
    user: UserSchema = Depends(get_current_active_user),
):
    """
    Update item in users cart

    Parameters
    ----------
        - user_id: users id, used for fetching and adding items to the cart
        - product_id: product_id, used for fetching and adding items to the cart
        - item_data: Hold information regarding update information
        - cart_service: Cart service used for getting cart information

    Returns
    -------
        A JSON response containing the cart information.

    """
    cart = await cart_service.update_cart_product(user.id, product_id, item_data)
    if not cart:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart item not found")
    return cart


@router.delete("/{product_id}", response_model=CartDetail)
async def remove_cart_product(
    product_id: int,
    cart_service: FromDishka[CartService],
    user: UserSchema = Depends(get_current_active_user),
):
    """
    Revome item from users cart

    Parameters
    ----------
        - user_id: users id, used for fetching and adding items to the cart
        - product_id: product_id, used for fetching product
        - cart_service: Cart service used for getting cart information

    Returns
    -------
        A JSON response containing the cart information.

    """
    cart = await cart_service.remove_cart_product(user.id, product_id)
    if not cart:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart item not found")
    return cart


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def clear_cart(
    cart_service: FromDishka[CartService], user: UserSchema = Depends(get_current_active_user)
):
    """Clear all items from the cart"""
    success = await cart_service.clear_cart(user.id)
    if not success:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error clearing cart")
