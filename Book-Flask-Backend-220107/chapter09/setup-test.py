import sys

from flask import Flask
from flask_script import Manager
from flask_twisted import Twisted
from twisted.python import log

app = Flask(__name__)


@app.route('/ping')
def hello():
    print('ping')
    return 'pong'


if __name__ == '__main__':
    twisted = Twisted(app)
    log.startLogging(sys.stdout)

    app.logger.info('Running the app...')
    manager = Manager(app)
    manager.run()


# FLASK_APP=setup-test.py flask run -h "0.0.0.0" -p 5000
# python setup-test.py
# python setup-test.py runserver -h "0.0.0.0" -p 5000 (flask_script)

