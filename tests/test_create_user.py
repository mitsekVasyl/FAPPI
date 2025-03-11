from tests.app import test_app


def test_create_user():
    user = {
        'username': 'test',
        'email': "vm.test@vm.com",
        'age': 43,
        'password': '1234'
    }
    response = test_app.post('/api/v1/users', json=user)

    print(response.json())
