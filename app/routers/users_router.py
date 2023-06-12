from fastapi import APIRouter, status, Depends
from databases import Database
from db.db_manager import get_db
from schemas import users_schemas
from services.user_service import UserService
from routers.depends import get_current_user, Paginator
from schemas.users_schemas import *

router = APIRouter(tags=['User'],)


@router.post('/user/', response_model=users_schemas.UserResponse, status_code=200)
async def create_user(user: users_schemas.SignUpRequest, db: Database = Depends(get_db)) -> UserResponse:
    user_service = UserService(db=db)
    db_user = await user_service.get_user_by_email(user_email=user.user_email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Email already registered.')
    created_user = await user_service.create_user(user=user)
    return users_schemas.UserResponse(result=created_user)


@router.get('/user/{user_id}/', response_model=users_schemas.UserResponse,
            dependencies=[Depends(get_current_user)], status_code=200)
async def get_user_by_id(user_id: int, db: Database = Depends(get_db)) -> UserResponse:
    user_service = UserService(db=db)
    user = await user_service.get_user_by_id(user_id=user_id)
    return UserResponse(result=user)


@router.get('/users/', response_model=users_schemas.UsersListResult,
            dependencies=[Depends(get_current_user)], status_code=200)
async def get_users_list(paginator_params: Paginator = Depends(), db: Database = Depends(get_db)) -> UsersListResult:
    user_service = UserService(db=db)
    users_list = await user_service.get_users_list(current_offset=paginator_params.get_current_offset(),
                                                   max_per_page=paginator_params.max_per_page)
    return UsersListResult(result=users_list)


@router.put('/user/{user_id}/', response_model=users_schemas.UserResponse, status_code=200)
async def update_user(user_id: int, user: users_schemas.UserUpdateRequest, db: Database = Depends(get_db),
                      current_user: User = Depends(get_current_user)) -> UserResponse:
    user_service = UserService(db=db)
    search_user = await user_service.validate_user(user_id=user_id, current_user=current_user)
    updated_user = await user_service.update_user(user_id=search_user.user_id, user_update=user)
    return UserResponse(result=updated_user)


@router.delete('/user/{user_id}/', response_model=users_schemas.User, status_code=200)
async def delete_user(user_id: int, db: Database = Depends(get_db),
                      current_user: User = Depends(get_current_user)) -> User:
    user_service = UserService(db=db)
    search_user = await user_service.validate_user(user_id=user_id, current_user=current_user)
    deleted_user = await user_service.delete_user(user_id=user_id, user_delete=search_user)
    return deleted_user

