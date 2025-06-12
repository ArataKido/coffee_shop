from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination import Page, paginate
from dishka.integrations.fastapi import FromDishka, DishkaRoute

from app.dependencies.auth_dependencies import get_current_active_user, user_is_admin
from app.schemas.user_schema import UserSchema, UserUpdateSchema
from app.services.user_service import UserService

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
    route_class=DishkaRoute
)


@router.get("/me", response_model=UserSchema)
async def current_user(user=Depends(get_current_active_user)):
    """
    Get information about current user

    Parameters
    ----------
        - user: current user, fetched from token

    """
    return user


@router.get("/", response_model=Page[UserSchema])
async def read_users(user_service: FromDishka[UserService], user=Depends(user_is_admin)):
    """
    Get all users, route for admins only

    Parameters
    ----------
        - user: used to check if the user is admin
        - user_service: User service used for fetching user

    """
    return paginate(await user_service.get_all_users())


@router.get("/{user_id}", response_model=UserSchema)
async def read_user(user_id: int, user_service: FromDishka[UserService]):
    """
    Gets user by id

    Parameters
    ----------
        - user_id: id of the user to be looked up
        - user_service: User service used for fetching user

    """
    user = await user_service.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.patch("/{user_id}", response_model=UserSchema)
async def patch_user(user_id: int, user_data: UserUpdateSchema, user_service: FromDishka[UserService]):
    """
    Partially updates user

    Parameters
    ----------
        - user_id: id of the user to be updated
        - user_service: User service used for updating user

    """
    updated_user = await user_service.patch_update_user(user_id, user_data)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found or update failed")
    return updated_user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, user_service: FromDishka[UserService]):
    """
    Soft deletes user

    Parameters
    ----------
        - user_id: id of user to be removed
        - user_service: User service used for soft deleting user

    """
    return await user_service.soft_delete_user(user_id=user_id)
