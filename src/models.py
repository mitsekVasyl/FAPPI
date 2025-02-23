from sqlalchemy import Column, Integer, VARCHAR
from sqlalchemy.orm import declarative_base

Base = declarative_base()
metadata = Base.metadata


class UserModel(Base):
    __tablename__ = 'users'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    username: str = Column(VARCHAR, unique=True, nullable=False)  # TODO: unique seems have no effect
    email: str = Column(VARCHAR, unique=True, nullable=False)
    first_name: str = Column(VARCHAR, nullable=True)
    last_name: str = Column(VARCHAR, nullable=True)
    age: int = Column(Integer, nullable=False)
    password: str = Column(VARCHAR, nullable=False)
    is_admin: bool = Column(Integer, nullable=False, default=False)
