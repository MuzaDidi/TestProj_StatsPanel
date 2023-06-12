from databases import Database
from db.db_manager import get_db
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from core.security import decode_access_token
from schemas.users_schemas import User
from services.user_service import UserService

import logging
import ssl

ssl._create_default_https_context = ssl._create_unverified_context
logger = logging.getLogger(__name__)
token_auth_scheme = HTTPBearer()


async def get_current_user(db: Database = Depends(get_db), token: str = Depends(token_auth_scheme)) -> User:
    user_service = UserService(db=db)
    user = await get_user_by_token(token=token.credentials, db=user_service)
    logger.info(f"getting the current user: {user.user_id}")
    return user


async def get_user_by_token(token: str, db: UserService) -> User:
    cred_exception = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Credentials are not valid")

    payload = decode_access_token(token=token)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid auth token")

    email = payload.get("sub")
    if email is None:
        raise cred_exception

    user = await db.get_user_by_email(user_email=email)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found user")

    return user


class Paginator:
    def __init__(self, page: int = 1, max_per_page: int = 10):
        self.page = page
        self.max_per_page = max_per_page

    def get_current_offset(self):
        current_offset = (self.page - 1) * self.max_per_page
        return current_offset
