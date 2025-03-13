from copy import deepcopy

import pytest
from sqlalchemy import text

from tests.app import engine, test_app


@pytest.fixture(scope='session', name='teardown_db')
def teardown_test_db_records():
    yield None # nothing to return for now

    with engine.connect() as connection:
        print("Deleting test record from users table")
        connection.execute(text('DELETE FROM users;'))
        connection.commit()


@pytest.fixture(scope='session', name='test_user_create_fxt')
def test_user_create():
    print('Creating test user create fixture.')
    user = {
        'username': 'vm',
        'email': "vm.test@vm.com",
        'first_name': 'v_test',
        'last_name': 'm_test',
        'age': 43,
        'password': '1234'
    }
    response = test_app.post('/api/v1/users', json=user)
    assert response.status_code == 201
    return user


@pytest.fixture(scope='session', name='test_user_update_fxt')
def test_user_update():
    print('Creating test user update fixture.')
    user = dict(
        username='test_user',
        email='test_user@example.com',
        first_name='User',
        last_name='Regular',
        age=21,
        password='1234'
    )
    print('Making a request')

    response = test_app.post('/api/v1/users', json=user)
    user['id'] = response.json()["id"]

    return user


@pytest.fixture(scope='session', name='test_user_get_fxt')
def test_user_get():
    print('Creating test user update fixture.')
    user = dict(
        username='test_user',
        email='test_user@example.com',
        first_name='User',
        last_name='Regular',
        age=21,
        password='1234'
    )

    for i in range(2):
        new_user = deepcopy(user)
        # update fields with unique constraint
        new_user['username'] = new_user['username'] + str(i)
        new_user['email'] = str(i) + new_user['email']
        test_app.post('/api/v1/users', json=new_user)

    return new_user
