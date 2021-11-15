"""
File used to create connections and run queries into database
"""
import sqlite3
from flask import current_app, g
from flaskapp import config
from typing import Optional


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


def register_user(username: str, password: str, is_trainer: str) -> Optional[str]:
    """
    Registers username with password if valid
    :param username: string with the username
    :param password: string with the password
    :param is_trainer: str whether the user is a trainer
    :return: error message if fail or None if success
    """
    conn = get_db()
    try:

        conn.execute("INSERT INTO user (u_name, u_password) VALUES (?, ?)",
                     (username, password))
        conn.commit()
        if is_trainer == 'on':
            conn.execute("""INSERT INTO trainer (t_userID)
                            Select u_userID from user
                            where u_name = ?
                            and u_password = ?""", (username, password))
            conn.execute("""UPDATE user
                            Set u_trainer = 1
                            where u_name = ?
                            and u_password = ?""", (username, password))
            conn.commit()
        else:
            conn.execute("""INSERT INTO customer (c_userID)
                            Select u_userID from user
                            where u_name = ?
                            and u_password = ?""", (username, password))
        close_db()
        return None
    except sqlite3.IntegrityError:
        error = f"Username {username} already exists"
        return error
    except Exception:
        error = "500 Internal Server Error"
        return error


def login_user(username: str, password: str) -> Optional[str]:
    """
    Verifies users exists in database
    :param username: string with the username
    :param password: string with the password
    :return: error message if fail or None if success
    """
    conn = get_db()
    error = None
    try:
        user_data = conn.execute("SELECT * FROM user WHERE u_name = ? "
                                 "AND u_password = ?",
                                 (username, password)).fetchone()
        print(user_data)
        close_db()
        if user_data is None:
            error = "Invalid credentials, please try again"
            return error
        else:
            return error
    except Exception:
        error = "500 Internal Server Error"
        return error

def get_exercises() -> Optional[str]:
    """
    returns all e_names from exercise table
    :return: list of exercise names
    """
    conn = get_db()
    error = None
    try:
        exercises = conn.execute("""SELECT e_name FROM exercise
                                 Order by e_name""").fetchall()
        # print(results)
        close_db()
        return exercises
    except Exception:
        error = "no exercises found"
        return error

def get_categories() -> Optional[str]:
    """
    returns all c_name from category table
    :return: list of category c_name
    """
    conn = get_db()
    error = None
    try:
        categories = conn.execute("""SELECT c_name FROM category
                                    Order by c_name""").fetchall()
        # print(results)
        close_db()
        return categories
    except Exception:
        error = "no categories found"
        return error
    
def get_trainers() -> Optional[str]:
    """
    returns all u_names of trainer from user table
    :return: list of trainer's u_name
    """
    conn = get_db()
    error = None
    try:
        exercises = conn.execute("""SELECT u_name FROM user, trainer
                                    where t_userID = u_userID
                                    Order by u_name""").fetchall()
        # print(results)
        close_db()
        return exercises
    except Exception:
        error = "no trainers found"
        return error