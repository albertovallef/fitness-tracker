"""
This file handles the authentication logic of the application
"""
from flask import (Blueprint, render_template, flash,
                   session, request, redirect, url_for)
from flaskapp import db


bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/')
@bp.route('/login', methods=('GET', 'POST'))
def login():
    """
    Checks for user in database and gives access to data while session last
    :return: html login template if fail or home template if success
    """
    if request.method == 'POST':
        user = request.form['user_name']
        password = request.form['user_password']
        resp = db.login_user(user, password)
        if resp is None:
            session['user'] = user
            session['password'] = password
            return redirect(url_for('home'))
        else:
            flash(resp, 'info')
            return redirect(url_for('auth.login'))
    else:
        return render_template('auth.html', type='Login')


@bp.route('/logout')
def logout():
    """
    Terminates session and redirects to login
    :return: html template of the login page
    """
    if 'user' in session:
        flash('You have been logout', 'info')
    session.pop('user', None)
    session.pop('password', None)
    return redirect(url_for('auth.login'))


@bp.route('/')
@bp.route('/register', methods=('GET', 'POST'))
def register():
    """
    Creates new user and saves it in the database
    :return: html template if login success or register template if fail
    """
    if request.method == 'POST':
        user = request.form['user_name']
        password = request.form['user_password']
        is_trainer = request.form.get('is_trainer')
        resp = db.register_user(user, password, is_trainer)
        if resp is None:
            resp = "You have been registered"
            flash(resp, 'info')
            return redirect(url_for('auth.login'))
        else:
            flash(resp, 'info')
            return redirect(url_for('auth.register'))
    else:
        return render_template('auth.html', type='Register')
