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
    subscription = trainers
    return render_template('subscription.html', trainers=trainers, subscriptions = subscription)
