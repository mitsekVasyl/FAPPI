from fastapi import status

from src.database import get_db_session

from tests.app import test_app


def test_db_connection():
    """Test that main database is available."""
    db_session = next(get_db_session())
    db_session.connection()
    db_session.close()


def test_heartbeat():
    """Test that health check endpoint returns success status with expected body."""
    response = test_app.get('/heartbeat')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'status': 'ok'}
