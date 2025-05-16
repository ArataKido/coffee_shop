from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination
from app.middleware.logging_middleware import LoggingMiddleware
from fastapi_pagination.utils import disable_installed_extensions_check

from app.routers import categories, products, orders, cart, auth, users

app = FastAPI(
    title="Coffee Shop API",
    description="API for Coffee Shop Management System",
    version="1.0.0",
    contact={
        "name": "Shahzod Ravshanov",
        "telegram" : "https://t.me/ArataKido"
    }
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(LoggingMiddleware)

# Include routers
app.include_router(categories.router)
app.include_router(products.router)
app.include_router(orders.router)
app.include_router(cart.router)
app.include_router(auth.router)
app.include_router(users.router)

add_pagination(app)
disable_installed_extensions_check()

