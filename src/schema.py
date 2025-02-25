from typing import Optional

from fastapi import Path
from pydantic import BaseModel, Field, EmailStr, ConfigDict

USERNAME_PATTERN = r'[A-Za-z0-9]+'

USER_ID_PATH_PARAM = Path(gt=0)


class UserQueryParams(BaseModel):
    model_config = ConfigDict(extra='forbid')

    id: Optional[str] = Field(gt=0, default=None)
    username: Optional[str] = Field(pattern=USERNAME_PATTERN, max_length=50, min_length=1, default=None)
    first_name: Optional[str] = Field(max_length=100, default=None)
    last_name: Optional[str] = Field(max_length=100, default=None)
    limit: int = Field(default=100)



class UserBaseSchema(BaseModel):
    username: str = Field(pattern=USERNAME_PATTERN, max_length=50)
    email: EmailStr = Field(max_length=100)
    first_name: Optional[str] = Field(max_length=100, default=None)
    last_name: Optional[str] = Field(max_length=100, default=None)
    age: int = Field(ge=0, le=150)


class UserResponseSchema(UserBaseSchema):
    id: int = Field(gt=0)


class UserCreateSchema(UserBaseSchema):
    model_config = ConfigDict(extra='forbid')

    password: str = Field(max_length=100)


class UserUpdateSchema(BaseModel):
    model_config = ConfigDict(extra='forbid')

    username: Optional[str] = Field(pattern=USERNAME_PATTERN, max_length=50, default=None)
    email: Optional[EmailStr] = Field(max_length=100, default=None)
    first_name: Optional[str] = Field(max_length=100, default=None)
    last_name: Optional[str] = Field(max_length=100, default=None)
    age: Optional[int] = Field(ge=0, le=150, default=None)
    password: Optional[str] = Field(max_length=100, default=None)
