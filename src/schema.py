from typing import Optional

from fastapi import Path
from pydantic import BaseModel, Field, EmailStr


USER_ID_PATTERN = r'[0-9]+'

USER_ID_PATH_PARAM = Path(pattern=USER_ID_PATTERN, min_length=1, max_length=50)


class UserQueryParams(BaseModel):
    id: Optional[str] = Field(pattern=USER_ID_PATTERN, max_length=100, min_length=1, default=None)
    username: Optional[str] = Field(pattern=r'[A-Za-z0-9]+', max_length=50, min_length=1, default=None)
    first_name: Optional[str] = Field(max_length=100, default=None)
    last_name: Optional[str] = Field(max_length=100, default=None)
    limit: int = Field(default=100)



class UserBaseSchema(BaseModel):
    username: str = Field(pattern=r'[A-Za-z0-9]+', max_length=50)
    email: EmailStr = Field(max_length=100)
    first_name: Optional[str] = Field(max_length=100, default=None)
    last_name: Optional[str] = Field(max_length=100, default=None)
    age: int = Field(ge=0, le=150)


class UserRequestSchema(UserBaseSchema):
    password: str = Field(max_length=100)