from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination import Page, paginate
from dishka.integrations.fastapi import FromDishka, DishkaRoute

from app.dependencies.auth_dependencies import get_current_active_user
from app.dependencies.dependencies import get_order_service
from app.models.order import OrderStatus
from app.schemas.order_schema import OrderCreate, OrderDetail, OrderInDB, OrderUpdate
from app.schemas.user_schema import UserSchema
from app.services.order_service import OrderService

router = APIRouter(
    prefix="/orders",
    tags=["orders"],
    responses={404: {"description": "Not found"}},
    route_class=DishkaRoute
)


@router.post("/", response_model=OrderDetail, status_code=status.HTTP_201_CREATED)
async def create_order(order: OrderCreate, order_service: FromDishka[OrderService]):
    """Create a new order"""
    created_order = await order_service.create_order(order)
    if not created_order:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Could not create order, check products exist"
        )
    return created_order


@router.get("/", response_model=Page[OrderInDB])
async def read_orders(
    order_service: FromDishka[OrderService],
    order_status: OrderStatus = None,
    user: UserSchema = Depends(get_current_active_user),
) -> Page[OrderInDB]:
    """Get all orders"""
    orders = await order_service.get_user_orders(user.id, order_status)
    return paginate(orders)


@router.get("/{order_id}", response_model=OrderDetail)
async def read_order(order_id: int, order_service: FromDishka[OrderService]):
    """Get an order by ID with items"""
    order = await order_service.get_order_by_id(order_id)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return order


@router.patch("/{order_id}", response_model=OrderInDB)
async def update_order(order_id: int, order: OrderUpdate, order_service: FromDishka[OrderService]):
    """Update an order's status"""
    updated_order = await order_service.update_order_status(order_id, order)
    if not updated_order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return updated_order


@router.delete("/{order_id}", response_model=OrderInDB)
async def delete_order(order_id: int, order_service: FromDishka[OrderService]):
    """Cancel an order"""
    success = await order_service.delete_order(order_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Order not found or cannot be cancelled")

    # Get updated order
    updated_order = await order_service.get_order_by_id(order_id)
    return updated_order
