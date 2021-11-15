"""
This file handles searching and adding workouts
"""
from flask import (Blueprint, render_template, flash,
                   session, request, redirect, url_for)
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
    return render_template('workout.html', exercises = exercises, categories = categories)


