from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.schemas.user import UserCreateSchema, UserSchema
from app.services.user_service import UserService
from app.dependencies import get_user_service

# Import routers
from app.routers import categories, products, orders, cart

app = FastAPI(
    title="Coffee Shop API",
    description="API for Coffee Shop Management System",
    version="1.0.0",
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

@app.get("/")
async def root():
    return {"message": "Welcome to Coffee Shop API"}

@app.post("/users/", response_model=UserSchema)
async def create_user(user: UserCreateSchema, user_service: UserService = Depends(get_user_service)):
    created_user = await user_service.create_user(user)
    if not created_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return created_user

@app.get("/users/{user_id}", response_model=UserSchema)
async def read_user(user_id: int, user_service: UserService = Depends(get_user_service)):
    user = await user_service.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/users/", response_model=list[UserSchema])
async def read_users(user_service: UserService = Depends(get_user_service)):
    return await user_service.get_all_users()
