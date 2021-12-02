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
    :return JSON response:
    """
    data = request.get_json()
    set_id = db.insert_set(data)
    db.insert_workout(session['training_session'], set_id, data)
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@bp.route('/training_session', methods=['GET', 'POST'])
def training_session():
    """
    Creates training sessions when user clicks start workout
    :return JSON response:
    """
    if request.method == 'POST':
        session['training_session'] = db.get_training_session(session['user'])
        resp = f"""Training session created with 
                ID#{session['training_session']}"""
    return json.dumps(resp), 200, {'ContentType': 'application/json'}


@bp.route('/search-by-cat', methods=['GET', 'POST'])
def return_by_cat():
    """
    Returns only exercises with a given category
    :return JSON response:
    """
    if request.method == 'POST':
        print('searching by category')
        data = request.get_json()
        # print(data)
        return db.get_exercises_by_cat(data)
        

