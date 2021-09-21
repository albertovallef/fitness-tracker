"""
This file starts and configures the flask application
"""
from flask import Flask, render_template

app = Flask(__name__, template_folder='static/templates')


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True)
