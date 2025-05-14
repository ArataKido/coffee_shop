from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.schemas.user import UserCreateSchema, UserSchema
from app.services.user_service import UserService
from app.dependencies import get_user_service
import logging

# Import routers
from app.routers import categories, products, orders, cart, auth, users

app = FastAPI(
    title="Coffee Shop API",
    description="API for Coffee Shop Management System",
    version="1.0.0",
    # swagger_ui_parameters={"docExpansion": "list", "tryItOutEnabled": True},
)

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


