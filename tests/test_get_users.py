from tests.app import test_app


def test_get_users_single_filter(test_user_get_fxt, teardown_db):
    query = {
        "username": test_user_get_fxt["username"],
    }
    response = test_app.get('/api/v1/users', params=query)
    body = response.json()

    assert response.status_code == 200
    assert len(body) == 1
    assert body[0]["username"] == test_user_get_fxt["username"]


def test_get_users_multi_filter(test_user_get_fxt, teardown_db):
    query = {
        "id": 1,
        "username": test_user_get_fxt["username"],
        "first_name": test_user_get_fxt["first_name"],
        "last_name": test_user_get_fxt["last_name"],
        "email": test_user_get_fxt["email"],
    }
    response = test_app.get('/api/v1/users', params=query)
    body = response.json()

    assert response.status_code == 200
    assert len(body) == 1
    assert body[0]["username"] == test_user_get_fxt["username"]
