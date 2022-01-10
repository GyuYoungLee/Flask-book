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
        'hashed_password': payload.get('password'),
        'profile': payload.get('profile')
    }

    app.users[app.id_count] = new_user
    app.id_count += 1

    return jsonify(new_user)


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

    app.tweets.append(new_tweet)
    return jsonify(app.tweets)


@app.route('/follow', methods=['POST'])
def follow():
    payload = request.json
    user_id = int(payload.get('id'))
    user_id_to_follow = int(payload.get('follow'))

    if user_id not in app.users:
        return 'no user', 400

    user = app.users.get(user_id)
    follow_list = user.setdefault('follow_list', [])
    if user_id_to_follow not in follow_list:
        follow_list.append(user_id_to_follow)

    return jsonify(user)


@app.route('/unfollow', methods=['GET'])
def unfollow():
    payload = request.json
    user_id = int(payload.get('id'))
    user_id_to_unfollow = int(payload.get('unfollow'))

    if user_id not in app.users:
        return 'no user', 400

    user = app.users.get(user_id)
    follow_list = user.setdefault('follow_list', [])
    if user_id_to_unfollow in follow_list:
        follow_list.remove(user_id_to_unfollow)

    return jsonify(user)


@app.route('/timeline/<int:user_id>', methods=['GET'])
def timeline(user_id):
    user = app.users.get(user_id)

    if user_id not in app.users:
        return 'no user', 400

    target_list = user.get('follow_list', []) + [user_id]
    timeline = [tweet for tweet in app.tweets if tweet.get('user_id') in target_list]

    return jsonify({
        'user_id': user_id,
        'timeline': timeline
    })


# http -v POST 127.0.0.1:5000/sign-up name=gy
# http -v POST 127.0.0.1:5000/sign-up name=jang
# http -v POST 127.0.0.1:5000/tweet id:=1 tweet="111"
# http -v POST 127.0.0.1:5000/tweet id:=2 tweet="222"
# http -v POST 127.0.0.1:5000/follow id:=1 follow:=2
# http -v GET 127.0.0.1:5000/timeline/1
