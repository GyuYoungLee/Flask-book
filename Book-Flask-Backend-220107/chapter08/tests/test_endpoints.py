import json
import bcrypt
import pytest
from sqlalchemy import create_engine, text
from ..app import create_app
from .test_config import DB_URL

database = create_engine(DB_URL, encoding='UTF-8', max_overflow=0)


@pytest.fixture
def api():
    app = create_app({'DB_URL': DB_URL})
    app.config['TESTING'] = True
    return app.test_client()


@pytest.fixture
def login(api):
    def _data(email, password):
        resp = api.post('/login',
                        data=json.dumps({'email': email, 'password': password}),
                        content_type='application/json')

        result = json.loads(resp.data.decode('UTF-8'))
        return result.get('access_token')

    return _data


def setup_function():
    new_user = {
        'name': 'test',
        'email': 'test',
        'hashed_password': bcrypt.hashpw(b'test', bcrypt.gensalt()),
        'profile': 'test'
    }
    database.execute(text("""
                INSERT INTO users(name, email, hashed_password, profile)
                VALUES (:name, :email, :hashed_password, :profile)
            """), new_user)


def teardown_function():
    database.execute(text("SET FOREIGN_KEY_CHECKS=0"))
    database.execute(text("truncate users"))
    database.execute(text("truncate tweets"))
    database.execute(text("truncate users_follow_list"))
    database.execute(text("SET FOREIGN_KEY_CHECKS=1"))


def test_1():
    assert 1 == 1

# def test_tweet(api, login):
#     access_token = login('gy', 'gy')
#     assert access_token is not None
