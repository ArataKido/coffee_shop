from dishka import Provider, Scope, provide, from_context
from app.repositories import (
    cart_repository,
    category_repository,
    order_repository,
    product_repository,
    user_repository,
)
from app.config import Config


class RepoProvider(Provider):
    config = from_context(provides=Config, scope=Scope.APP)
    scope = Scope.REQUEST

    get_user_repo = provide(user_repository.UserRepository, scope=scope.REQUEST)
    get_cart_repository = provide(cart_repository.CartRepository)
    get_category_repository = provide(category_repository.CategoryRepository)
    get_order_repository = provide(order_repository.OrderRepository)
    get_product_repository = provide(product_repository.ProductRepository)
