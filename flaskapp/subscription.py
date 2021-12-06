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
    trainers = db.get_non_subscribed_trainers(session['user'])
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

    db.subscribe(session['user'], trainer)

    trainers = db.get_non_subscribed_trainers(session['user'])
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

    trainers = db.get_non_subscribed_trainers(session['user'])
    subscription = db.get_subs(session['user'])

    return json.dumps((trainers, subscription))

@bp.route('view_progress_table', methods=['GET', 'POST'])
def view_progress_table():
    """
    Serves data(date completed, exercise name, reps, weight) to the js progress
    to built the progress table showing
    :return: json response
    """
    data = request.get_json()
    # print('data',data)
    exercise_table_data = db.get_all_exercises_from_dates(data['trainer'],
                                                           data['start_date'],
                                                           data['end_date'])
    # print(exercise_table_data)
    return json.dumps(exercise_table_data), 200, {
            'ContentType': 'application/json'}
