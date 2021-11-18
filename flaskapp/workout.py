"""
This file handles searching and adding workouts
"""
from flask import (Blueprint, render_template, flash,
                   session, request, redirect, url_for, json)
from flaskapp import db

bp = Blueprint('workout', __name__, url_prefix='/workout')


@bp.route('/')
def workout():
    """
    Page where user adds workouts
    :return: html workout template with exercises in search bar
    """
    exercises = db.get_exercises()
    categories = db.get_categories()
    return render_template('workout.html', exercises=exercises,
                           categories=categories)


@bp.route('/add_workout', methods=['POST'])
def add_workout():
    """
    Add workout to database when user clicks button
    :return:
    """
    data = request.get_json()
    set_id = db.insert_set(data)
    db.insert_workout(session['training_session'], set_id, data)
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@bp.route('/add_workout', methods=['POST'])
def add_set():
    """
    Add set to database when user clicks button
    :return:
    """
    return None


