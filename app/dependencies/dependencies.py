from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.repositories.cart_repository import CartRepository
from app.repositories.category_repository import CategoryRepository
from app.repositories.order_repository import OrderRepository
from app.repositories.product_repository import ProductRepository
from app.repositories.user_repository import UserRepository
from app.services.cart_service import CartService
from app.services.category_service import CategoryService
from app.services.email_service import EmailService
from app.services.order_service import OrderService
from app.services.product_service import ProductService
from app.services.user_service import UserService


async def get_user_repository(db: AsyncSession = Depends(get_db)) -> UserRepository:
    return UserRepository(db)


async def get_cart_repository(db: AsyncSession = Depends(get_db)) -> CartRepository:
    return CartRepository(db)


async def get_category_repository(db: AsyncSession = Depends(get_db)) -> CategoryRepository:
    return CategoryRepository(db)


async def get_product_repository(db: AsyncSession = Depends(get_db)) -> ProductRepository:
    return ProductRepository(db)


async def get_order_repository(db: AsyncSession = Depends(get_db)) -> OrderRepository:
    return OrderRepository(db)


async def get_user_service(user_repo: UserRepository = Depends(get_user_repository)) -> UserService:
    return UserService(db=user_repo.db, user_repository=user_repo)


async def get_cart_service(
    cart_repo: CartRepository = Depends(get_cart_repository),
    product_repo: CartRepository = Depends(get_product_repository),
) -> CartService:
    return CartService(db=cart_repo.db, cart_repository=cart_repo, product_repository=product_repo)


async def get_category_service(category_repo: CategoryRepository = Depends(get_category_repository)) -> CategoryService:
    return CategoryService(db=category_repo.db, category_repository=category_repo)


async def get_product_service(
    product_repo: ProductRepository = Depends(get_product_repository),
    category_repo: CategoryRepository = Depends(get_category_repository),
) -> ProductService:
    return ProductService(db=product_repo.db, product_repository=product_repo, category_repository=category_repo)


async def get_order_service(
    order_repo: OrderRepository = Depends(get_order_repository),
    product_repo: ProductRepository = Depends(get_product_repository),
) -> OrderService:
    return OrderService(db=order_repo.db, order_repository=order_repo, product_repository=product_repo)


async def get_auth_service(user_service: UserService = Depends(get_user_service)):
    from app.services.auth_service import AuthService

    return AuthService(user_service=user_service)


async def get_oauth_scheme():
    return OAuth2PasswordBearer(tokenUrl="auth/login")


def get_email_service():
    return EmailService()
