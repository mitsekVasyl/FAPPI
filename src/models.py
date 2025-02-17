from pydantic import BaseModel, Field, EmailStr


class UserRequestModel(BaseModel):
    username: str = Field(pattern=r'[A-Za-z0-9]+', max_length=50)
    email: EmailStr = Field(max_length=100)
    first_name: str = Field(max_length=100)
    last_name: str = Field(max_length=100)
    age: int = Field(ge=0, le=150)
    password: str = Field(max_length=100)
