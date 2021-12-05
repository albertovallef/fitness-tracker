"""
This file handles the subscribtion logic of the application
"""
from flask import (Blueprint, render_template, flash,
                   session, request, redirect, url_for, json)
from flaskapp import db


bp = Blueprint('subscription', __name__, url_prefix='/subscription')

@bp.route('/', methods=('GET', 'POST'))
def subscription():
    """
    Page where users add trainers
    :return: html progress template
    """
    trainers = db.get_trainers()
    subscription = db.get_subs(session['user'])
    print(subscription)
    return render_template('subscription.html', trainers=trainers, subscriptions = subscription)

@bp.route('/subscribe', methods=('GET', 'POST'))
def subscribe():
    """
    Page where users add trainers
    :return: html progress template
    """
    trainer = request.get_json()
    print(trainer)

    trainers = db.get_trainers()
    db.subscribe(session['user'], trainer)
    subscription = db.get_subs(session['user'])

    return json.dumps((trainers, subscription))

@bp.route('/unsubscribe', methods=('GET', 'POST'))
def unsubscribe():
    """
    Page where users add trainers
    :return: html progress template
    """
    trainer = request.get_json()
    print(trainer)
    
    db.unsubscribe(session['user'], trainer)
    trainers = db.get_trainers()
    subscription = db.get_subs(session['user'])

    return json.dumps((trainers, subscription))

