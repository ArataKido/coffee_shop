# from typing_extensions import Any
from dishka import Provider, Scope, provide, from_context, provide_all

from app.services import (
    cart_service,
    category_service,
    email_service,
    order_service,
    product_service,
    user_service,
    auth_service,
)
from app.utils.loggers.logger import Logger
from app.config import Config


class ServiceProvider(Provider):
    config = from_context(provides=Config, scope=Scope.APP)
    scope = Scope.REQUEST

    # get_user_service = provide(user_service.UserService(app_config=self.config.app))
    # @provide()
    # def get_user_service(self, config:Config) -> user_service.UserService:
    #     return user_service.UserService(app_config=config.app)

    @provide(scope=scope.APP)
    def get_logger(self, config:Config) -> Logger:
        return Logger(config.app)

    interaction = provide_all(
        cart_service.CartService,
        category_service.CategoryService,
        email_service.EmailService,
        product_service.ProductService,
        auth_service.AuthService,
        user_service.UserService,
    )
    # get_cart_service = provide(cart_service.CartService)
    # get_category_service = provide(category_service.CategoryService)
    # get_email_service = provide(email_service.EmailService)
    # get_order_service = provide(order_service.OrderService)
    # get_product_service = provide(product_service.ProductService)
    # get_auth_service = provide(auth_service.AuthService)
    # get_auth_service = provide(auth_service.AuthService)
