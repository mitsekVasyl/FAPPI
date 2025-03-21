from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.models import Base

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

SessionLocal = sessionmaker(bind=engine)

def create_db_and_tables():
    Base.metadata.create_all(engine)


def get_db_session():
    with SessionLocal() as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db_session)]
