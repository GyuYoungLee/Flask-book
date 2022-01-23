from flask import Flask, request, jsonify, current_app
from sqlalchemy import create_engine, text


def insert_user(user):
    return current_app.database.execute(text("""
            INSERT INTO users(name, email, hashed_password, profile)
            VALUES (:name, :email, :hashed_password, :profile)
        """), user).lastrowid


def get_user(user_id):
    row = current_app.database.execute(text("""
                SELECT id, name, email, profile, created_at
                FROM users
                WHERE id = :id
            """), {'id': user_id}).fetchone()

    return {
        'id': row['id'],
        'name': row['name'],
        'email': row['email'],
        'profile': row['profile'],
        'created_at': row['created_at'].strftime('%Y-%m-%d %H:%M:%S')
    } if row else None


def insert_tweet(tweet):
    return current_app.database.execute(text("""
            INSERT INTO tweets (user_id, tweet)
            VALUES (
                :user_id,
                :tweet
            )
        """), tweet).lastrowid


def get_tweet(tweet_id):
    row = current_app.database.execute(text("""
        SELECT id, user_id, tweet, created_at
        FROM tweets
        WHERE id = :id
    """), {'id': tweet_id}).fetchone()

    return {
        'id': row['id'],
        'user_id': row['user_id'],
        'tweet': row['tweet'],
        'created_at': row['created_at'].strftime('%Y-%m-%d %H:%M:%S')
    } if row else None


def insert_follow(follow):
    return current_app.database.execute(text("""
            INSERT INTO users_follow_list(user_id, follow_user_id)
            VALUES (:user_id, :follow_user_id)
        """), follow).rowcount


def get_follow(follow):
    row = current_app.database.execute(text("""
        SELECT user_id, follow_user_id
        FROM users_follow_list
        WHERE user_id = :user_id and follow_user_id = :follow_user_id
    """), follow).fetchone()

    return {
        'id': row['user_id'],
        'follow': row['follow_user_id']
    } if row else None


def delete_follow(unfollow):
    return current_app.database.execute(text("""
            DELETE FROM users_follow_list
            WHERE user_id = :user_id AND follow_user_id = :follow_user_id
        """), unfollow).rowcount


def get_timeline(user_id):
    rows = current_app.database.execute(text("""
        SELECT t.user_id, t.tweet
        FROM tweets t
            LEFT JOIN users_follow_list ufl ON t.user_id = ufl.follow_user_id
        WHERE ufl.user_id = :user_id OR t.user_id = :user_id  
    """), {'user_id': user_id})

    return [{'user_id': row['user_id'], 'tweet': row['tweet']} for row in rows]


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    app.database = create_engine(app.config.get('DB_URL'), encoding='utf-8', max_overflow=0)

    @app.route('/sign-up', methods=['POST'])
    def sign_up():
        payload = request.json
        new_user = {
            'name': payload.get('name'),
            'email': payload.get('email'),
            'hashed_password': payload.get('password'),
            'profile': payload.get('profile')
        }

        new_user_id = insert_user(new_user)

        new_user = get_user(new_user_id)
        return jsonify(new_user)

    @app.route('/tweet', methods=['POST'])
    def tweet():
        payload = request.json
        new_tweet = {
            'user_id': int(payload.get('id')),
            'tweet': payload.get('tweet')
        }

        if len(new_tweet['tweet']) > 10:
            return 'tweet should be within 10', 400

        new_tweet_id = insert_tweet(new_tweet)

        new_tweet = get_tweet(new_tweet_id)
        return jsonify(new_tweet)

    @app.route('/follow', methods=['POST'])
    def follow():
        payload = request.json
        follow = {
            'user_id': int(payload.get('id')),
            'follow_user_id': int(payload.get('follow'))
        }

        insert_follow(follow)

        new_follow = get_follow(follow)
        return jsonify(new_follow)

    @app.route('/unfollow', methods=['POST'])
    def unfollow():
        payload = request.json
        unfollow = {
            'user_id': int(payload.get('id')),
            'follow_user_id': int(payload.get('unfollow'))
        }

        delete_follow(unfollow)

        current_follow = get_follow(unfollow)
        return jsonify(current_follow)

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

        return jsonify({
            'user_id': user_id,
            'timeline': get_timeline(user_id)
        })

    return app
