"""
This file starts and configures the flask application
"""
from flask import Flask, render_template, session, redirect, url_for
from flaskapp import auth, db, workout, progress, subscription


app = Flask(__name__, template_folder='static/templates')
app.config.from_mapping(
        SECRET_KEY='dev'
    )
app.register_blueprint(auth.bp)
app.register_blueprint(workout.bp)
app.register_blueprint(progress.bp)
app.register_blueprint(subscription.bp)

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

if __name__ == '__main__':
    app.run(debug=True)
