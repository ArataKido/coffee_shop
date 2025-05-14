from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination import Page, paginate
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.dependencies.auth_dependencies import get_current_active_user, user_is_admin
from app.schemas.order import OrderCreate, OrderUpdate, OrderInDB, OrderDetail
from app.schemas.user import UserCreateSchema, UserSchema, UserUpdateSchema
from app.services.order_service import OrderService
from app.repositories.order_repository import OrderStatus
from app.dependencies.dependencies import get_order_service, get_user_service
from app.services.user_service import UserService

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

@router.get('/me', response_model=UserSchema)
async def current_user(user = Depends(get_current_active_user)):
    return user

@router.get('/', response_model=Page[UserSchema])
async def read_users(user_service: UserService = Depends(get_user_service), user = Depends(user_is_admin)):
    return paginate(await user_service.get_all_users())

@router.get("/{user_id}", response_model=UserSchema)
async def read_user(user_id: int, user_service: UserService = Depends(get_user_service)):
    user = await user_service.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post('/', response_model=UserSchema)
async def create_user(user: UserCreateSchema, user_service: UserService = Depends(get_user_service)):
    created_user = await user_service.create_user(user)
    if not created_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return created_user

@router.patch('/{user_id}', response_model=UserSchema)
async def patch_user(user_id: int, user_data: UserUpdateSchema, user_service: UserService = Depends(get_user_service)):
    updated_user = await user_service.patch_update_user(user_id, user_data)  
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found or update failed")
    return updated_user

@router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, user_service: UserService = Depends(get_user_service)):
    return await user_service.soft_delete_user(user_id=user_id)