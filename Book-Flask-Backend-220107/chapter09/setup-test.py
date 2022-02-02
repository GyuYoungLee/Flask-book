from flask import Flask

app = Flask(__name__)


@app.route('/ping')
def hello():
    print('ping')
    return 'pong'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


# FLASK_APP=setup.py flask run -h "0.0.0.0" -p 5000
# python setup.py
