"""
This file handles the view progress logic of the application such as
rendering a graph for a selected exercise from a date range, also it
displays the workout data in a table
"""
from flask import (Blueprint, render_template, flash,
                   session, request, redirect, url_for, json)
from flaskapp import db


bp = Blueprint('progress', __name__, url_prefix='/progress')


@bp.route('/', methods=['GET', 'POST'])
def progress():
    """
    Page shows users their fitness progress
    :return: html progress template
    """
    exercises = db.get_user_exercises(session['user'])
    categories = db.get_categories()
    return render_template('progress.html', exercises=exercises,
                           categories=categories)


@bp.route('/view_progress', methods=['GET', 'POST'])
def view_progress():
    """
    Serves data(date, average weight) to the js progress for the selected
    exercise within the given date range
    :return: json response
    """
    data = request.get_json()
    exercise_data = db.get_exercise_data(data, session['user'])
    return json.dumps(exercise_data), 200, {
        'ContentType': 'application/json'}


@bp.route('view_progress_table', methods=['GET', 'POST'])
def view_progress_table():
    """
    Serves data(date completed, exercise name, reps, weight) to the js progress
    to built the progress table showing
    :return: json response
    """
    data = request.get_json()
    exercise_table_data = db.get_exercise_table_from_dates(session['user'],
                                                           data['exercise'],
                                                           data['start_date'],
                                                           data['end_date'])
    return json.dumps(exercise_table_data), 200, {
            'ContentType': 'application/json'}
