"""
File used to create connections and run queries into database
"""
import sqlite3
from flask import current_app, g
from flaskapp import config
from typing import Optional, Dict
from datetime import date


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
    except sqlite3.Error as error:
        print(error)
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
        close_db()
        if user_data is None:
            error = "Invalid credentials, please try again"
            return error
        else:
            return error
    except sqlite3.Error as error:
        print(error)
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
    except sqlite3.Error as error:
        print(error)
        return error


def get_exercises_by_cat(category: str) -> Optional[str]:
    """
    returns all e_names from exercise table
    :return: list of exercise names
    """
    conn = get_db()
    error = None
    try:
        # print(type(category))
        exercises = conn.execute("""SELECT e_name FROM exercise, ex_cat, category
                                    where c_name = ?
                                    and c_categoryID = ec_categoryID
                                    and e_exerciseID = ec_exerciseID
                                    Order by e_name""", (category,)).fetchall()
        print(exercises)
        close_db()
        return exercises
    except sqlite3.Error as error:
        print(error)
        return error


def get_user_exercises(user_name: str) -> Optional[str]:
    """
    returns all e_names from exercise table from a specific user
    :return: list of exercise names
    """
    conn = get_db()
    error = None
    try:
        exercises = conn.execute("""SELECT DISTINCT e_name
                              FROM user, training_session, 
                                   workout, exercise
                             WHERE u_userID = r_userID AND 
                                   r_sessionID = w_sessionID AND 
                                   w_exerciseID = e_exerciseID AND 
                                   u_name = ?;""", (user_name, )).fetchall()
        close_db()
        return exercises
    except sqlite3.Error as error:
        print(error)
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
    except sqlite3.Error as error:
        print(error)
        return error


def get_trainers() -> Optional[str]:
    """
    returns all u_names of trainer from user table
    :return: list of trainer's u_name
    """
    conn = get_db()
    error = None
    try:
        trainers = conn.execute("""SELECT u_name FROM user, trainer
                                    where t_userID = u_userID
                                    Order by u_name COLLATE NOCASE""").fetchall()
        # print(results)
        close_db()
        return trainers
    except sqlite3.Error as error:
        print(error)
        return error


def get_non_subscribed_trainers(user) -> Optional[str]:
    """
    returns all trainers the user is not subscrbed to
    """
    conn = get_db()
    error = None
    try:
        trainers = conn.execute("""SELECT distinct u_name FROM user, trainer
                                    where t_userID = u_userID
                                    and u_trainer = 1
                                    and u_name NOT IN (
                                        SELECT u2.u_name FROM user u1, user u2, trainer, customer, subscription
                                        where c_userID = u1.u_userID
                                        and u1.u_name = ?
                                        and su_customerID = c_customerID
                                        and t_trainerID = su_trainerID 
                                        and u2.u_userID = t_userID
                                    )
                                    Order by u_name COLLATE NOCASE""", (user,)).fetchall()
        # print(trainers)
        close_db()
        return trainers
    except sqlite3.Error as error:
        print(error)
        return error


def get_subs(user) -> Optional[str]:
    """
    returns all trainers the user is subscribed to
    """
    conn = get_db()
    error = None
    try:
        trainers = conn.execute("""SELECT u2.u_name FROM user u1, user u2, trainer, customer, subscription
                                    where c_userID = u1.u_userID
                                    and u1.u_name = ?
                                    and su_customerID = c_customerID
                                    and t_trainerID = su_trainerID 
                                    and u2.u_userID = t_userID
                                    Order by u2.u_name COLLATE NOCASE""", (user,)).fetchall()
        # print(results)
        close_db()
        return trainers
    except sqlite3.Error as error:
        print(error)
        return error


def subscribe(user, trainer) -> Optional[str]:
    """
    subscribes the given user and trainer
    """
    conn = get_db()
    error = None
    try:
        print(user,trainer)
        conn.execute("""
                    INSERT INTO subscription (su_trainerID, su_customerID)
                    select t_trainerID, c_customerID from
                    (Select t_trainerID from user, trainer where t_userID = u_userID and u_name = ?),
                    (select c_customerID from user, customer where u_userID = c_userID and u_name = ?);
                    """, (trainer,user))
        conn.commit()
        close_db()
        return None
    except sqlite3.Error as error:
        print(error)
        return error


def unsubscribe(user, trainer) -> Optional[str]:
    """
    unsubscribes a user from a trainer
    """
    conn = get_db()
    error = None
    try:
        print(user,trainer)
        conn.execute("""
                DELETE FROM subscription
                WHERE su_trainerID IN (
                    SELECT t_trainerID
                    FROM user, trainer
                    WHERE u_userID = t_userID
                    and u_name = ?
                )
                AND
                su_customerID IN (
                    SELECT c_customerID
                    FROM user, customer
                    WHERE u_userID = c_userID
                    and u_name = ?)
                    """, (trainer,user))
        conn.commit()
        close_db()
        return None
    except sqlite3.Error as error:
        print(error)
        return error


def get_training_session(user: str) -> Optional[str]:
    """
    Gets the training id from training session table or creates one if there
    is not one already created or todays session is complete
    :param user: user name in session
    :return: None or the training session id
    """
    conn = get_db()
    try:
        today = date.today().strftime('%Y-%m-%d')
        training_session = conn.execute("""SELECT r_sessionID
                                          FROM training_session,
                                               user
                                         WHERE r_userID = u_userID AND
                                               r_status = 0 AND
                                               u_name = ? AND
                                               r_datecompleted = ?;""",
                                        (user, today)).fetchone()
        close_db()
        if training_session is None:
            training_session = insert_training_session(user)
            return training_session
        return training_session[0]
    except sqlite3.Error as error:
        print(error)
        return None


def insert_training_session(user: str):
    """
    Inserts a new session in the training session and returns the id
    :param user: user name in session
    :return: training session id or error if any
    """
    conn = get_db()
    try:
        today = date.today().strftime('%Y-%m-%d')

        conn.execute("""INSERT INTO training_session (r_userID, r_status, r_datecompleted)
                    SELECT u_userID, 0, ?  FROM user
                        WHERE u_name = ?;""", (today, user))
        conn.commit()
        close_db()
        return get_training_session(user)
    except sqlite3.Error as error:
        print(error)
        return error


def insert_set(data: Dict) -> str:
    """
    Inserts data into the sets database and returns the set id
    :param data: dictionary with the exe name, reps, wight, and duration data
    :return: id of the created row or None of success
    """
    conn = get_db()
    try:
        conn.execute("""INSERT INTO sets (s_reps, s_weight, s_duration) 
                        VALUES (?, ?, ?);""", (data['reps'], data['weight'],
                                               data['duration']))
        conn.commit()
        set_id = conn.execute("""SELECT MAX(s_setID) FROM sets;""").fetchone()
        close_db()
        return set_id[0]
    except sqlite3.Error as error:
        print(error)
        return None


def insert_workout(training_session_id: str, set_id: str, data: Dict) -> Optional[str]:
    """
    Insert data into the workout table
    :param training_session_id: training session in the session app
    :param set_id: set of id of the just inserted set
    :param data: dictionary with the exe name, reps, wight, and duration data
    :return: None or error
    """
    conn = get_db()
    try:
        conn.execute("""INSERT into workout (w_sessionID, w_exerciseID, w_setID)
                        SELECT ?, e_exerciseID, ? FROM 
                        (SELECT e_exerciseID FROM exercise 
                            WHERE e_name = ?);""", (training_session_id, set_id,
                                                    data['exercise']))
        conn.commit()
        close_db()
        return None
    except sqlite3.Error as error:
        print(error)
        return error


def get_exercise_data(data: Dict, user: str) -> Optional[Dict]:
    conn = get_db()
    try:
        exe_data = conn.execute("""SELECT AVG(s_weight), r_datecompleted
                              FROM user,
                                   training_session, workout, sets, exercise
                             WHERE u_userID = r_userID AND
                                   w_setID = s_setID AND
                                   w_sessionID = r_sessionID AND
                                   w_exerciseID = e_exerciseID AND
                                   u_name = ? AND
                                   e_name = ? AND
                                   r_datecompleted BETWEEN ? AND ?
                                   group by r_datecompleted;""",
                                (user, data['exercise'],
                                 data['start_date'], data['end_date'])).fetchall()
        close_db()
        data_dict = [dict([('weight', row[0]), ('date', row[1])]) for row in exe_data]
        return data_dict
    except sqlite3.Error as error:
        print(error)
        return None


def get_exercise_table_from_dates(user: str, exercise: str,
                                  start: str, end: str) -> Optional[Dict]:
    conn = get_db()
    try:
        exe_data = conn.execute("""SELECT r_datecompleted, e_name, 
                                          s_reps, s_weight
                                  FROM training_session,
                                       exercise, sets,
                                       workout, user
                                 WHERE w_sessionID = r_sessionID AND
                                       w_exerciseID = e_exerciseID AND
                                       w_setID = s_setID AND
                                       u_userID = r_userID AND
                                       u_name = ? AND
                                       e_name = ? AND
                                       r_datecompleted BETWEEN ? AND ?
                                 GROUP BY s_setID
                                 ORDER BY r_datecompleted DESC;""",
                                (user, exercise, start, end)).fetchall()
        close_db()
        data_dict = [dict([('Date', row[0]), ('Exercise', row[1]),
                           ('Reps', row[2]), ('Weight', row[3])]) for row in exe_data]
        return data_dict
    except sqlite3.Error as error:
        print(error)
        return None


def get_all_exercises_from_dates(user: str, start: str, end: str) -> Optional[Dict]:
    conn = get_db()
    try:
        exe_data = conn.execute("""SELECT r_datecompleted, e_name, 
                                          s_reps, s_weight
                                  FROM training_session,
                                       exercise, sets,
                                       workout, user
                                 WHERE w_sessionID = r_sessionID AND
                                       w_exerciseID = e_exerciseID AND
                                       w_setID = s_setID AND
                                       u_userID = r_userID AND
                                       u_name = ? AND
                                       r_datecompleted BETWEEN ? AND ?
                                 GROUP BY s_setID
                                 ORDER BY r_datecompleted DESC;""",
                                (user, start, end)).fetchall()
        close_db()
        data_dict = [dict([('Date', row[0]), ('Exercise', row[1]),
                           ('Reps', row[2]), ('Weight', row[3])]) for row in exe_data]
        return data_dict
    except sqlite3.Error as error:
        print(error)
        return None

def get_body_data(user: str) -> Optional[str]:
    conn = get_db()
    try:
        data = conn.execute("""
                            SELECT b_age, b_gender, b_height, b_weight
                            FROM body, user
                            WHERE u_userID = b_userID AND
                            u_name = ?;
                            """
                            ,(user,)).fetchall()
        close_db()
        return data
    except sqlite3.Error as error:
        print(error)
        return None

def update_body(user, stat, value) -> Optional[str]:
    """
    Update the body of the given user
    :param user: the user whose body will be updated
    :param stat: the stat that will be changed, must be b_weight, b_age, or b_height
    :param value: new value
    :return: None or error
    """
    conn = get_db()
    try:
        # if stat not in ['b_height','b_weight','b_age']:
        #     print('ERROR: not a valid stat')
        #     return None
        query = """
                UPDATE body
                SET """ + stat + """ = ?
                FROM user
                WHERE b_userID = u_userID AND
                    u_name = ?;
                """
        data = conn.execute(query
                            ,( value ,user))
        conn.commit()
        close_db()
        return data
    except sqlite3.Error as error:
        print(error)
        return None
