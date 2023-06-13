from starlette import status

from core.security import get_hash_password
from databases import Database
from sqlalchemy import select, insert, update, delete
from schemas.users_schemas import *
from db.models import UsersTable

import logging


logger = logging.getLogger(__name__)


class UserService:
    def __init__(self, db: Database):
        self.db = db

    async def validate_user(self, user_id: int, current_user: User) -> User:
        """Validating the user."""
        search_user = await self.get_user_by_id(user_id=user_id)
        if search_user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} not found.")
        if search_user.user_id != current_user.user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="It's not your account")
        return search_user

    async def get_user_by_email(self, user_email: str, with_secret_info: bool = False) -> Optional[User | UserBase]:
        """Getting user by email."""
        query_user = select(UsersTable).where(UsersTable.user_email == user_email)
        user_data = await self.db.fetch_one(query=query_user)
        if user_data:
            user = UserBase.parse_obj(user_data) if with_secret_info else User.parse_obj(user_data)
            logger.info(f"user getting by email: {user.user_email}")
        else:
            user = None
        return user

    async def get_user_by_id(self, user_id: int) -> User:
        """Getting user by id."""
        query_user = select(UsersTable).where(UsersTable.user_id == user_id)
        user_data = await self.db.fetch_one(query=query_user)
        if user_data is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This user not found")
        user = User.parse_obj(user_data)
        logger.info(f"user getting by id: {user.user_id}")
        return user

    async def get_users_list(self, current_offset: int, max_per_page: int) -> UsersListResponse:
        """Getting list of users."""
        query_users = select(UsersTable).order_by(UsersTable.user_id).limit(max_per_page).offset(current_offset)
        users_data = await self.db.fetch_all(query=query_users)
        users_list = [User.parse_obj(user) for user in users_data]
        if users_list is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Users not found.")
        users = UsersListResponse(users=users_list)
        return users

    async def create_user(self, user: SignUpRequest) -> User:
        """Create a new user."""
        user.validate_name(user.user_name)
        user.validate_password(user.user_password)
        user.validate_password_repeat(user.user_password_repeat, {'user_password': user.user_password})

        user_create = UsersTable(
            user_email=user.user_email,
            user_name=user.user_name,
            user_role=RoleEnum.user,
            user_hashed_password=get_hash_password(user.user_password_repeat),
            user_created_at=datetime.utcnow(),
            user_updated_at=datetime.utcnow(),
        )

        user_dict = user_create.dict()
        query_user = insert(UsersTable).values(user_dict).returning(UsersTable.user_id)
        user_data = await self.db.fetch_one(query=query_user)

        user_result = User(
            user_id=user_data['user_id'],
            user_email=user_create.user_email,
            user_name=user_create.user_name,
            user_created_at=user_create.user_created_at,
            user_updated_at=user_create.user_updated_at,
        )
        logger.info(f"user created with id: {user_result.user_id}")
        return user_result

    async def update_user(self, user_id: int, user_update: UserUpdateRequest) -> User:
        """Updating of existing user."""
        user_dict = {}
        if user_update.user_name:
            user_update.validate_name(user_update.user_name)
            user_dict['user_name'] = user_update.user_name
        if user_update.user_password:
            user_update.validate_password(user_update.user_password)
            user_update.validate_password_repeat(user_update.user_password_repeat,
                                                 {'user_password': user_update.user_password})
            user_dict['user_hashed_password'] = get_hash_password(user_update.user_password_repeat)
        user_dict['user_updated_at'] = datetime.utcnow()

        query_user = update(UsersTable).where(UsersTable.user_id == user_id).values(**user_dict).returning(UsersTable)
        user_data = await self.db.fetch_one(query=query_user)
        user = User.parse_obj(user_data)
        logger.info(f"user updated with id: {user.user_id}")
        return user

    async def delete_user(self, user_id: int, user_delete: User) -> User:
        """Deleting user by id."""
        query_user = delete(UsersTable).where(UsersTable.user_id == user_id)
        await self.db.fetch_one(query=query_user)
        logger.info(f"user deleted with id: {user_id}")
        return user_delete
