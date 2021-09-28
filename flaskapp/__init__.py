"""
This file starts and configures the flask application
"""
from flask import Flask, render_template
from flaskapp import auth


app = Flask(__name__, template_folder='static/templates')
app.register_blueprint(auth.bp)

@app.route('/')
def home():
    return render_template('home.html', title='Home')


if __name__ == '__main__':
    app.run(debug=True)
