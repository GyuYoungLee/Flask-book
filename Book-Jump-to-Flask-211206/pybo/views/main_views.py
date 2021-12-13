from flask import Blueprint, url_for
from werkzeug.utils import redirect

bp = Blueprint('main', __name__, url_prefix='/')


@bp.route('/')
def index():
    # return redirect('/question/list/')
    return redirect(url_for('question._list'))
