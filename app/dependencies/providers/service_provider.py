# from typing_extensions import Any
from dishka import Provider, Scope, provide, from_context

from app.services import (
    cart_service,
    category_service,
    email_service,
    order_service,
    product_service,
    user_service,
)
from app.utils.loggers.logger import Logger
from app.config import Config


class ServiceProvider(Provider):
    config = from_context(provides=Config, scope=Scope.APP)
    scope = Scope.REQUEST

    # get_user_service = provide(user_service.UserService(app_config=self.config.app))
    @provide()
    def get_user_service(self, config:Config) -> user_service.UserService:
        return user_service.UserService(app_config=self.config.app)

    @provide(scope=scope.APP)
    def get_logger(self, config:Config) -> Logger:
        return Logger(config.app)

    # get_user_service = provide(user_service.UserService)
    get_cart_service = provide(cart_service.CartService)
    get_category_service = provide(category_service.CategoryService)
    get_email_service = provide(email_service.EmailService)
    get_order_service = provide(order_service.OrderService)
    get_product_service = provide(product_service.ProductService)
    # get_logger = provide(Logger, scope=scope.APP)
