from copy import deepcopy

import pytest

from tests.app import test_app


def create_user_validation_cases():
    invalid_cases = (
        ({'username': 564738}, 'Input should be a valid string'),
        # ({'username': "()special"}, ''),  # TODO: fails
        ({'username': "a" * 51}, 'String should have at most 50 characters'),
        ({'email': "not_email"}, 'value is not a valid email address: An email address must have an @-sign.'),
        ({'email': ("e" * 100) + "mail@mail.mail"}, 'value is not a valid email address: The email address is too long '
                                                    'before the @-sign (40 characters too many).'),
        ({'first_name': "a" * 101}, 'String should have at most 100 characters'),
        ({'last_name': "a" * 101}, 'String should have at most 100 characters'),
        ({'age': 'not numeric'}, 'Input should be a valid integer, unable to parse string as an integer'),
        ({'age': -13}, 'Input should be greater than or equal to 0'),
    )
    for case, expected_msg in invalid_cases:
        yield case, expected_msg


@pytest.mark.parametrize('fields_to_update, expected_msg', create_user_validation_cases())
def test_create_user_bad_input(fields_to_update, expected_msg, test_user_create_fxt, teardown_db):
    """Test that update user data is validated as expected."""
    user = deepcopy(test_user_create_fxt)
    user.update(fields_to_update)

    response = test_app.post('/api/v1/users', json=user)

    body = response.json()
    assert response.status_code == 422
    assert body['detail'][0]['msg'] == expected_msg


def test_create_user_all_fields(test_user_create_fxt, teardown_db):
    """Test that user is created."""
    user = deepcopy(test_user_create_fxt)
    user.update({'username': 'frankenstain', 'email': 'franki@example.com'})
    response = test_app.post('/api/v1/users', json=user)

    body = response.json()
    assert response.status_code == 201
    assert body['username'] == user['username']


def test_create_user_conflict(test_user_create_fxt, teardown_db):
    """Test that user with the same username or email cannot be created."""
    response = test_app.post('/api/v1/users', json=test_user_create_fxt)

    body = response.json()
    assert response.status_code == 409
    assert body['detail'] == 'User already exists.'
