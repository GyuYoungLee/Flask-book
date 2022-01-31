import json
import pytest
import bcrypt
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
        if not resp.data:
            return None

        result = json.loads(resp.data.decode('UTF-8'))
        return result.get('access_token')

    return _data


def setup_function():
    users = [
        {
            'name': 'test1',
            'email': 'test1',
            'hashed_password': bcrypt.hashpw(b'test', bcrypt.gensalt()),
            'profile': 'test'
        },
        {
            'name': 'test2',
            'email': 'test2',
            'hashed_password': bcrypt.hashpw(b'test', bcrypt.gensalt()),
            'profile': 'test'
        }
    ]

    tweets = [
        {
            'user_id': 2,
            'tweet': 'Hello World'
        }
    ]

    database.execute(text("""
        INSERT INTO users(name, email, hashed_password, profile)
        VALUES (:name, :email, :hashed_password, :profile)
    """), users)

    database.execute(text("""
        INSERT INTO tweets(user_id, tweet)
        VALUES (:user_id, :tweet)
    """), tweets)


def teardown_function():
    database.execute(text("SET FOREIGN_KEY_CHECKS=0"))
    database.execute(text("truncate users"))
    database.execute(text("truncate tweets"))
    database.execute(text("truncate users_follow_list"))
    database.execute(text("SET FOREIGN_KEY_CHECKS=1"))


def test_me():
    assert 1 == 1


def test_ping(api):
    resp = api.get('/ping')
    assert resp.data == b'pong'


def test_unauthorized(api):
    tweet = {'tweet': 'hi'}
    follow = {'follow': 2}
    unfollow = {'unfollow': 2}

    resp = api.post('/tweet',
                    data=json.dumps(tweet),
                    content_type='appliaction/json')
    assert resp.status_code == 401

    resp = api.post('/follow',
                    data=json.dumps(follow),
                    content_type='application/json')
    assert resp.status_code == 401

    resp = api.post('/unfollow',
                    data=json.dumps(unfollow),
                    content_type='application/json')
    assert resp.status_code == 401


def test_tweet(api, login):
    user = {
        'email': 'test1',
        'password': 'test'
    }
    tweet = {'tweet': 'hi'}

    # tweet
    access_token = login(user['email'], user['password'])
    resp = api.post('/tweet',
                    data=json.dumps(tweet),
                    content_type='application/json',
                    headers={'Authorization': access_token})

    assert resp.status_code == 200

    # tweet 확인
    resp = api.get('/timeline/1')
    result = json.loads(resp.data.decode('UTF-8'))

    assert resp.status_code == 200
    assert result == {
        'user_id': 1,
        'timeline': [{
            'user_id': 1,
            'tweet': 'hi'
        }]
    }


def test_follow(api, login):
    user = {
        'email': 'test1',
        'password': 'test'
    }
    follow = {'follow': 2}

    # follow
    access_token = login(user['email'], user['password'])
    resp = api.post('/follow',
                    data=json.dumps(follow),
                    content_type='application/json',
                    headers={'Authorization': access_token})

    assert resp.status_code == 200

    # follow 확인
    resp = api.get('/timeline/1')
    result = json.loads(resp.data.decode('UTF-8'))

    assert resp.status_code == 200
    assert result == {
        'user_id': 1,
        'timeline': [{
            'user_id': 2,
            'tweet': 'Hello World'
        }]
    }


def test_unfollow(api, login):
    user = {
        'email': 'test1',
        'password': 'test'
    }
    follow = {'follow': 2}
    unfollow = {'unfollow': 2}

    # follow
    access_token = login(user['email'], user['password'])
    resp = api.post('/follow',
                    data=json.dumps(follow),
                    content_type='application/json',
                    headers={'Authorization': access_token})

    assert resp.status_code == 200

    # unfollow
    resp = api.post('/unfollow',
                    data=json.dumps(unfollow),
                    content_type='application/json',
                    headers={'Authorization': access_token})

    assert resp.status_code == 200

    # unfollow 확인
    resp = api.get('/timeline/1')
    result = json.loads(resp.data.decode('UTF-8'))

    assert resp.status_code == 200
    assert result == {
        'user_id': 1,
        'timeline': []
    }
