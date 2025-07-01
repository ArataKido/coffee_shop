from app.dependencies.auth_dependencies import user_is_admin
from app.schemas.category_schema import CategoryCreate, CategoryInDB, CategoryUpdate
from app.services.category_service import CategoryService
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination import Page, paginate
from dishka.integrations.fastapi import FromDishka, DishkaRoute

router = APIRouter(
    prefix="/categories", tags=["categories"], responses={404: {"description": "Not found"}}, route_class=DishkaRoute
)


@router.post("/", response_model=CategoryInDB, status_code=status.HTTP_201_CREATED)
async def create_category(
    category: CategoryCreate,
    category_service: FromDishka[CategoryService],
    user=Depends(user_is_admin),
):
    """Create a new category"""
    created_category = await category_service.create_category(category)
    if not created_category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Could not create category, it may already exist"
        )
    return created_category


@router.get("/", response_model=Page[CategoryInDB])
async def read_categories(category_service: FromDishka[CategoryService]):
    """Get all categories"""
    categories = await category_service.get_all_categories()
    if not categories:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categories were not found")
    return paginate(categories)


@router.get("/{category_id}", response_model=CategoryInDB)
async def read_category(category_id: int, category_service: FromDishka[CategoryService]):
    """Get a category by ID"""
    category = await category_service.get_category_by_id(category_id)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return category


@router.patch("/{category_id}", response_model=CategoryInDB)
async def update_category(
    category_id: int,
    category: CategoryUpdate,
    category_service: FromDishka[CategoryService],
    user=Depends(user_is_admin),
):
    """Update a category"""
    updated_category = await category_service.update_category(category_id, category)
    if not updated_category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return updated_category


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: int,
    category_service: FromDishka[CategoryService],
    user=Depends(user_is_admin),
):
    """Soft deletes a category"""
    success = await category_service.delete_category(category_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
