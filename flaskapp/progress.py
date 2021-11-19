"""
This file handles the view progress logic of the application such as
rendering a graph for a selected exercise from a date range, also it
displays the workout data in a table
"""
from flask import (Blueprint, render_template, flash,
                   session, request, redirect, url_for, json)
from flaskapp import db


bp = Blueprint('progress', __name__, url_prefix='/progress')


@bp.route('/', methods=('GET', 'POST'))
def progress():
    """
    Page shows users their fitness progress
    :return: html progress template
    """
    exercises = db.get_exercises()
    categories = db.get_categories()
    return render_template('progress.html', exercises=exercises,
                           categories=categories)


@bp.route('/view_progress', methods=('GET', 'POST'))
def view_progress():
    """
    Displays chart for the selected exercise within the date range
    :return:
    """
    data = request.get_json()
    print(data)
    return json.dumps({'success': True}), 200, {
        'ContentType': 'application/json'}