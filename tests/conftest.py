import pytest
from sqlalchemy import text

from tests.app import engine


@pytest.fixture(scope='session', name='teardown_db')
def teardown_test_db_records():
    yield None # nothing to return for now

    with engine.connect() as connection:
        print("Deleting test record from users table")
        connection.execute(text('DELETE FROM users;'))
        connection.commit()
