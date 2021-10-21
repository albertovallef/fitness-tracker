"""
File used to create connections and run queries into database
"""
import sqlite3
from flask import current_app, g
from flaskapp import config


def init_db():
    """
    Initializes the database using the schema.sql
    """
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


def get_db():
    """
    Opens connection to the database
    :return: database instance
    """
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(config.DATABASE)
    return db


def close_db(e=None):
    """
    Used to close database after committing
    :param e: Errors if any
    """
    db = g.pop('db', None)

    if db is not None:
        db.close()






