from flask import Flask, request, jsonify
from sqlalchemy import create_engine, text


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    database = create_engine(app.config.get('DB_URL'), encoding='utf-8', max_overflow=0)
    app.database = database

    @app.route('/sign-up', methods=['POST'])
    def sign_up():
        payload = request.json
        new_user = {
            'name': payload.get('name'),
            'email': payload.get('email'),
            'hashed_password': payload.get('password'),
            'profile': payload.get('profile', '')
        }

        new_user_id = app.database.execute(text("""
            INSERT INTO users(name, email, hashed_password, profile)
            VALUES (:name, :email, :hashed_password, :profile)
        """), new_user).lastrowid

        row = app.database.execute(text("""
            SELECT id, name, email, profile
            FROM users
            WHERE id = :user_id        
        """), {'user_id': new_user_id}).fetchone()

        created_user = {
            'id': row['id'],
            'name': row['name'],
            'email': row['email'],
            'profile': row['profile']
        } if row else None

        return jsonify(created_user)

    @app.route('/tweet', methods=['POST'])
    def tweet():
        payload = request.json
        user_id = int(payload.get('id'))
        tweet = payload.get('tweet')

        if len(tweet) > 10:
            return '10 over', 400

        new_tweet = {
            'user_id': user_id,
            'tweet': tweet
        }

        app.database.execute(text('''
            INSERT INTO tweets (user_id, tweet)
            VALUES (
                :user_id,
                :tweet
            )
        '''), new_tweet)

        return '', 200

    @app.route('/timeline/<int:user_id>', methods=['GET'])
    def timeline(user_id):
        # select user_id, tweet
        # from tweets
        # where user_id = 1
        #   or user_id in (select follow_user_id from users_follow_list where user_id = 1);

        # select t.user_id, t.tweet
        # from tweets t
        #   left join users_follow_list ufl on ufl.follow_user_id = t.user_id
        # where t.user_id = 1 or ufl.user_id = 1;

        rows = app.database.execute(text('''
            SELECT t.w
        '''))


    return app


# http -v POST 127.0.0.1:5000/sign-up name=gy email=gy
# http -v POST 127.0.0.1:5000/tweet id:=1 tweet="111"
