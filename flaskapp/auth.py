from flask import (Blueprint, render_template,
                   session, request, redirect, url_for)
from flaskapp import db


bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/')
@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        user = request.form['user_name']
        password = request.form['user_password']
        session['user'] = user
        return redirect(url_for('home'))
    else:
        return render_template('auth.html', type='Login')

@bp.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))



@bp.route('/')
@bp.route('/register', methods=('GET', 'POST'))
def register():
    con = db.get_db()
    return render_template('auth.html', type='Register')
