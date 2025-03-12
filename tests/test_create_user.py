from copy import deepcopy

import pytest

from tests.app import test_app


def get_user_dict_w_all_attrs():
    return {
        'username': 'test_user',
        'email': "vm.test@vm.com",
        'first_name': 'v_test',
        'last_name': 'm_test',
        'age': 43,
        'password': '1234'
    }


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
        user = deepcopy(get_user_dict_w_all_attrs())
        user.update(case)
        yield user, expected_msg


def test_create_user_all_fields(teardown_db):
    user = get_user_dict_w_all_attrs()
    response = test_app.post('/api/v1/users', json=user)

    body = response.json()
    assert response.status_code == 201
    assert body['username'] == user['username']


@pytest.mark.parametrize('user,expected_msg', create_user_validation_cases())
def test_create_user_bad_input(user, expected_msg, teardown_db):

    response = test_app.post('/api/v1/users', json=user)

    body = response.json()
    assert response.status_code == 422
    assert body['detail'][0]['msg'] == expected_msg
