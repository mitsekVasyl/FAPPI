from copy import deepcopy
from unittest.mock import Mock, patch

import pytest

from tests.app import test_app
from tests.test_create_user import create_user_validation_cases


@pytest.mark.parametrize('fields_to_update, expected_msg', create_user_validation_cases())
def test_update_user_bad_input(fields_to_update, expected_msg, teardown_db, test_user_update_fxt):
    """Test that update user data is validated as expected."""
    user = deepcopy(test_user_update_fxt)
    user.update(fields_to_update)

    response = test_app.put(f'/api/v1/users/{user["id"]}', json=fields_to_update)
    body = response.json()

    assert response.status_code == 422
    assert body['detail'][0]['msg'] == expected_msg


@pytest.mark.parametrize('fields_to_upd', (
        {'username': 'userupdated'}, {'email': 'updated@example.com'}, {'first_name': None}, {'first_name': 'updated'},
        {'last_name': None}, {'last_name': 'updated_last'}, {'age': 66}, {'password': '12345'}
))
@patch('src.users.authorize_user_request', Mock())
def test_update_user_valid_input(fields_to_upd, test_user_update_fxt: dict, teardown_db):
    """Test that user attributes are updated."""
    user = test_user_update_fxt
    user.update(fields_to_upd)
    user.pop('password', None)

    response = test_app.put(f'/api/v1/users/{user["id"]}', json=fields_to_upd)
    body = response.json()
    print(body)
    assert response.status_code == 200
    assert body == user
