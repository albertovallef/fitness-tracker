"""
This file starts and configures the flask application
"""
from flask import Flask, render_template, session, redirect, url_for
from flaskapp import auth, db


app = Flask(__name__, template_folder='static/templates')
app.config.from_mapping(
        SECRET_KEY='dev'
    )
app.register_blueprint(auth.bp)
with app.app_context():
    db.init_db()


@app.route('/')
def home():
    if 'user' in session:
        render_template(home)
    else:
        return redirect(url_for('auth.login'))


if __name__ == '__main__':
    app.run(debug=True)
