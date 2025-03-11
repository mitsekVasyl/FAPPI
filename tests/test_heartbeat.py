from fastapi.testclient import TestClient
from fastapi import status

from src.app import app


tc = TestClient(app)


def test_heartbeat():
    """Test that health check endpoint returns success status with expected body."""
    response = tc.get('/heartbeat')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'status': 'ok'}
