"""
This file starts and configures the flask application
"""
from flask import Flask, render_template, session, redirect, url_for
from flaskapp import auth, db, workout


app = Flask(__name__, template_folder='static/templates')
app.config.from_mapping(
        SECRET_KEY='dev'
    )
app.register_blueprint(auth.bp)
app.register_blueprint(workout.bp)

with app.app_context():
    db.init_db()


@app.route('/')
def home():
    """
    Home page where we welcome user and where workouts can be added
    :return: html login template if not session active or home page if session
    """
    if 'user' in session:
        return render_template('home.html', text=f"Welcome {session['user']}")
    else:
        return redirect(url_for('auth.login'))

@app.route('/')
def workout():
    """
    Page where user adds workouts
    :return: html workout template with exercises in search bar
    """
    return redirect(url_for('workout'))

@app.route('/progress', methods=('GET', 'POST'))
def progress():
    """
    Page where users view progress
    :return: html progress template
    """
    return render_template('progress.html')

@app.route('/trainers', methods=('GET', 'POST'))
def trainers():
    """
    Page where users add trainers
    :return: html progress template
    """
    trainers = db.get_trainers()
    return render_template('trainers.html', trainers = trainers)


if __name__ == '__main__':
    app.run(debug=True)
