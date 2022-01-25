from flask import Flask, request, jsonify

app = Flask(__name__)
app.id_count = 1
app.users = {}  # users 테이블
app.tweets = []  # tweets 테이블


@app.route('/sign-up', methods=['POST'])
def sign_up():
    payload = request.json
    new_user = {
        'id': app.id_count,
        'name': payload.get('name'),
        'email': payload.get('email'),
        'hashed_password': payload.get('passowrd'),
        'profile': payload.get('profile')
    }

    app.users[app.id_count] = new_user
    new_user_id = app.id_count
    app.id_count += 1

    return jsonify(app.users[new_user_id])


@app.route('/tweet', methods=['POST'])
def tweet():
    payload = request.json
    new_tweet = {
        'user_id': int(payload.get('id')),
        'tweet': payload.get('tweet')
    }

    if len(new_tweet['tweet']) > 10:
        return 'tweet should be within 10', 400

    app.tweets.append(new_tweet)

    return jsonify(app.tweets[-1])


@app.route('/follow', methods=['POST'])
def follow():
    payload = request.json
    user_id = int(payload.get('id'))
    user_id_to_follow = int(payload.get('follow'))

    if user_id not in app.users:
        return 'no user', 400

    follow_list = app.users.get(user_id).setdefault('follow_list', [])
    if user_id_to_follow not in follow_list:
        follow_list.append(user_id_to_follow)

    return jsonify(app.users.get(user_id))


@app.route('/unfollow', methods=['POST'])
def unfollow():
    payload = request.json
    user_id = int(payload.get('id'))
    user_id_to_unfollow = int(payload.get('unfollow'))

    if user_id not in app.users:
        return 'no user', 400

    follow_list = app.users.get(user_id).setdefault('follow_list', [])
    if user_id_to_unfollow in follow_list:
        follow_list.remove(user_id_to_unfollow)

    return jsonify(app.users.get(user_id))


@app.route('/timeline/<int:user_id>', methods=['GET'])
def timeline(user_id):
    if user_id not in app.users:
        return 'no user', 400

    user_id_list = [user_id] + app.users.get(user_id).get('follow_list', [])

    return jsonify({
        'user_id': user_id,
        'timeline': [x for x in app.tweets if x['user_id'] in user_id_list]
    })
