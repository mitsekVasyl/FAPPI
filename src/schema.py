from typing import Optional

from pydantic import BaseModel, Field, EmailStr


class UserQueryParams(BaseModel):
    id: Optional[str] = Field(pattern=r'[0-9]+', max_length=100, min_length=1, default=None)
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