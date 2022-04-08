from flask import Flask, render_template
from flask_login import login_required, current_user
from __init__ import db

master = Flask(__name__)

@master.route('/')
def index():
    return render_template('index.html')

@master.route('/resources')
def resources():
    return render_template('resources.html')

@master.route('/signup')
def signup():
    return render_template('signup.html')

@master.route('/calender')
def calender():
    return render_template('calender.html')

@master.route('/about')
def about():
    return render_template('about.html')

@master.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

# error handling
@master.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

@master.errorhandler(404)
def server_error(e):
    return render_template('404.html'), 404
