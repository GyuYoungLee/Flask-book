import json
import pytest
from sqlalchemy import create_engine, text
from app import create_app
import config

database = create_engine(config.test_config.get('DB_URL'), encoding='UTF-8', max_overflow=0)


@pytest.fixture
def api():
    app = create_app()
    app.config['TESTING'] = True
    return app.test_client()


def test_tweet(api):
    # 1. new_user
    # new_user = {
    #     'name': 'aa',
    #     'email': 'aa',
    #     'password': 'aa'
    # }
    # resp = api.post('/sign-up',
    #                 data=json.dumps(new_user),
    #                 content_type='application/json')
    #
    # assert resp.status_code == 200

    # 2. login
    login_info = {
        'email': 'aa',
        'password': 'aa'
    }
    resp = api.post('/login',
                    data=json.dumps(login_info),
                    content_type='application/json')

    result = json.loads(resp.data.decode('UTF-8'))
    access_token = result.get('access_token')

    # 3. tweet
    # tweet = {'tweet': 'hi'}
    # headers = {'Authorization': access_token}
    # resp = api.post('/tweet',
    #                 data=json.dumps(tweet),
    #                 content_type='application/json',
    #                 headers=headers)
    #
    # assert resp.status_code == 200

    # 4. tweet 확인
    headers = {'Authorization': access_token}
    resp = api.get(f'/timeline',
                   headers=headers)

    result = json.loads(resp.data.decode('UTF-8'))
    assert result == {
        'user_id': 2,
        'timeline': [{
            'user_id': 2,
            'tweet': 'hi'
        }]
    }
