from flask import Blueprint, render_template


bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/')
@bp.route('/login', methods=('GET', 'POST'))
def login():
    return render_template('auth.html', type='Login')

@bp.route('/')
@bp.route('/register', methods=('GET', 'POST'))
def register():
    return render_template('auth.html', type='Register')
