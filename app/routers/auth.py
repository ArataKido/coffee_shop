from fastapi import APIRouter, Depends, Security
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


from app.dependencies.auth_dependencies import get_auth_service
from app.schemas.token import Token
from app.schemas.user import UserCreateSchema, UserSchema
from app.services.auth_service import AuthService
from app.utils.security import oauth2_scheme

router = APIRouter(
    prefix="/auth", 
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)

@router.post("/signup", response_model=UserSchema)
async def signup(user: UserCreateSchema, auth_service: AuthService = Depends(get_auth_service)):
    return await auth_service.signup(user)  

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), auth_service: AuthService = Depends(get_auth_service)):
    return await auth_service.login(form_data.username, form_data.password)  

@router.post("/refresh", response_model=Token)
async def refresh_token(token: str = Security(oauth2_scheme), auth_service: AuthService = Depends(get_auth_service)):
    return await auth_service.refresh_token(token)  

@router.get("/verify")
async def verify(activation_code:str, auth_service: AuthService = Depends(get_auth_service)):
    return await auth_service.activate_user(activation_code)