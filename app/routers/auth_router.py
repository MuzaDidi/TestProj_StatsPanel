from fastapi import APIRouter, status, Depends
from schemas import users_schemas
from services.user_service import UserService
from core.security import validate_password, create_access_token
from db.db_manager import get_db
from databases import Database

from routers.depends import get_current_user
from schemas.users_schemas import *

router = APIRouter(prefix='/auth', tags=['Auth'])


@router.post('/login/', response_model=users_schemas.TokenResponse, status_code=200)
async def login(login: users_schemas.SignInRequest, db: Database = Depends(get_db)) -> TokenResponse:
    user_service = UserService(db=db)
    user = await user_service.get_user_by_email(user_email=login.user_email, with_secret_info=True)
    if user is None or not validate_password(password=login.user_password, hashed_password=user.user_hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Incorrect username or password')
    token = users_schemas.Token(access_token=create_access_token({"sub": login.user_email}), token_type="Bearer")
    return TokenResponse(result=token)


@router.get("/me/", response_model=users_schemas.UserResponse, status_code=200)
async def get_user_by_token(current_user: User = Depends(get_current_user)) -> UserResponse:
    return users_schemas.UserResponse(result=current_user)
