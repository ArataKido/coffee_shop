from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination
from fastapi_pagination.utils import disable_installed_extensions_check
from dishka.integrations.fastapi import setup_dishka
from fastapi_swagger_dark import get_swagger_ui_html

from app.dependencies.container import create_container
from app.middleware.logging_middleware import LoggingMiddleware  # noqa: F401
from app.routers import auth, cart, categories, orders, products, users


app = FastAPI(
    title="Coffee Shop API",
    description="API for Coffee Shop Management System",
    version="1.0.0",
    contact={"name": "Shahzod Ravshanov", "telegram": "https://t.me/ArataKido"},
)

app.add_middleware(LoggingMiddleware)  # noqa: ERA001
# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(categories.router)
app.include_router(products.router)
app.include_router(orders.router)
app.include_router(cart.router)
app.include_router(auth.router)
app.include_router(users.router)


setup_dishka(container=create_container(), app=app)
add_pagination(app)
disable_installed_extensions_check()



