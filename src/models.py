from typing import Optional

from pydantic import BaseModel, Field, EmailStr


class UserRequestModel(BaseModel):
    username: str = Field(pattern=r'[A-Za-z0-9]+', max_length=50)
    email: EmailStr = Field(max_length=100)
    first_name: Optional[str] = Field(max_length=100, default=None)
    last_name: Optional[str] = Field(max_length=100, default=None)
    age: int = Field(ge=0, le=150)
    password: str = Field(max_length=100)
