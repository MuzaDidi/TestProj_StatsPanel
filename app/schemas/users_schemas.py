import re
from datetime import datetime
from typing import Optional, List

from fastapi import HTTPException
from pydantic import BaseModel, EmailStr, validator
from db.models import RoleEnum


class ValidationMixin:
    LETTER_MATCH_PATTERN = re.compile(r'^[a-zA-Z0-9.\s@]+$')

    @validator("user_name", allow_reuse=True)
    def validate_name(cls, value):
        if not cls.LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="Name should contains only letters and numbers"
            )
        return value

    @validator("user_password", allow_reuse=True)
    def validate_password(cls, value):
        if len(value) < 8:
            raise HTTPException(
                status_code=422, detail="Password should contain at least 8 characters"
            )
        return value

    @validator("user_password_repeat", allow_reuse=True)
    def validate_password_repeat(cls, value, values):
        if value != values["user_password"]:
            raise HTTPException(
                status_code=422, detail="Passwords do not match"
            )
        return value


class User(BaseModel):
    user_id: int
    user_email: EmailStr
    user_name: str
    user_role: RoleEnum = RoleEnum.user
    user_created_at: datetime
    user_updated_at: datetime


class UserBase(User):
    user_hashed_password: str


class SignInRequest(BaseModel):
    user_email: EmailStr
    user_password: str


class SignUpRequest(BaseModel, ValidationMixin):
    user_email: EmailStr
    user_name: str
    user_password: str
    user_password_repeat: str

    class Config:
        validate_assignment = True
        arbitrary_types_allowed = True


class UserUpdateRequest(BaseModel, ValidationMixin):
    user_name: Optional[str] = None
    user_password: Optional[str] = None
    user_password_repeat: Optional[str] = None

    class Config:
        validate_assignment = True
        arbitrary_types_allowed = True


class UsersListResponse(BaseModel):
    users: List[User] = []

    class Config:
        orm_mode = True


class UsersListResult(BaseModel):
    result: UsersListResponse

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    result: User


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenResponse(BaseModel):
    result: Token
