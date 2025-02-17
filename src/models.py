from typing import Optional

from pydantic import BaseModel, Field, EmailStr
from sqlalchemy import Column, Integer, VARCHAR
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class UserBaseModel(BaseModel):
    username: str = Field(pattern=r'[A-Za-z0-9]+', max_length=50)
    email: EmailStr = Field(max_length=100)
    first_name: Optional[str] = Field(max_length=100, default=None)
    last_name: Optional[str] = Field(max_length=100, default=None)
    age: int = Field(ge=0, le=150)


class UserRequestModel(UserBaseModel):
    password: str = Field(max_length=100)


class UserDBModel(Base):
    __tablename__ = 'users'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    username: str = Column(VARCHAR, unique=True, nullable=False)  # TODO: unique seems have no effect
    email: EmailStr = Column(VARCHAR, unique=True, nullable=False)
    first_name: str = Column(VARCHAR, nullable=True)
    last_name: str = Column(VARCHAR, nullable=True)
    age: int = Column(Integer, nullable=False)
    password: str = Column(VARCHAR, nullable=False)
