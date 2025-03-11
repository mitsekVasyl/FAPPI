from fastapi import status
from tests.app import test_app

def test_heartbeat():
    """Test that health check endpoint returns success status with expected body."""
    response = test_app.get('/heartbeat')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'status': 'ok'}
