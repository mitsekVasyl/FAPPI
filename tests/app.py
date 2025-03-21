from fastapi.testclient import TestClient

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.app import app
from src.auth.auth_utils import verify_access_token
from src.database import get_db_session
from src.models import Base


sqlite_url = "sqlite:///test_database.db"

engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})
TestSessionLocal = sessionmaker(bind=engine)

Base.metadata.create_all(engine)


def get_test_db_session():
    with TestSessionLocal() as session:
        yield session


def verify_access_token_override():
    return {"user_id": 10007, 'is_admin': True}


app.dependency_overrides = {
    get_db_session: get_test_db_session,
    verify_access_token: verify_access_token_override
}

test_app = TestClient(app)
