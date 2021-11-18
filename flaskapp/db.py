"""
File used to create connections and run queries into database
"""
import sqlite3
from flask import current_app, g
from flaskapp import config
from typing import Optional, Dict


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


def register_user(username: str, password: str, is_trainer: str, b_age: int, b_height: int, b_weight: int, b_gender: str) -> Optional[str]:
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

        conn.execute("""INSERT INTO body (b_userID, b_age, b_gender, b_height, b_weight) 
                        Select 
                        (SELECT u_userID from user
                            where u_name = ?
                            and u_password = ?), ?,?,?,?""",
                     (username, password, b_age, b_gender, b_height, b_weight))
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
            conn.commit()
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


def insert_set(data: Dict) -> str:
    """
    Insert data into the sets database
    FIXME: We could do a check in the table for data with the same parameters
    FIXME: Add if statement that checks for same data if not create instance
    :param data: dictionary with the exe name, reps, wight, and duration data
    :return: id of the created row or None of success
    """
    conn = get_db()
    error = None
    try:
        conn.execute("""INSERT INTO sets (s_reps, s_weight, s_duration) 
                        VALUES (?, ?, ?);""", (data['reps'], data['weight'],
                                               data['duration']))
        conn.commit()
        set_id = conn.execute("""SELECT MAX(s_setID) FROM sets;""").fetchone()
        close_db()
        return set_id[0]
    except Exception:
        error = "Error inserting set"
        return error


def insert_workout(user: str, set_id: str, data: Dict) -> Optional[str]:
    """
    Insert data into the workout table
    :param user: name of the user in session
    :param set_id: set of id of the just inserted set
    :param data: dictionary with the exe name, reps, wight, and duration data
    :return: None or error
    """
    print("Hellow world")
    conn = get_db()
    error = None
    try:
        sql = ("""INSERT into workout (w_sessionID, w_exerciseID, w_setID)
                SELECT r_sessionID, e_exerciseID, ? FROM 
                (SELECT r_sessionID FROM training_session, user 
                    WHERE r_userID = u_userId AND u_name = ? AND 
                    r_status = 0), 
                (SELECT e_exerciseID FROM exercise 
                    WHERE e_name = ?);""", (set_id, user, data['exercise']))
        conn.execute(sql)
        conn.commit()
        close_db()
        return None
    except Exception:
        error = "Error inserting workout"
        print(error)
        return error
