from flask import Blueprint, render_template
from flask_login import login_required, current_user

master = Blueprint('master', __name__)

@master.route('/')
def index():
    return render_template('index.html')

@master.route('/signup')
def signup():
    return render_template('signup.html')

@master.route('/calendar')
def calendar():
    return render_template('calendar.html')

@master.route('/profile')
@login_required
def profile():
    return render_template('profile.html',
                           name=current_user.name,
                           phonenumber=current_user.phonenumber,
                           email=current_user.email,
                           pronouns=current_user.pronouns,
                           gender=current_user.gender,
                           attraction=current_user.attraction,
                           bio=current_user.bio,
                           )

# error handling
@master.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

@master.errorhandler(404)
def server_error(e):
    return render_template('404.html'), 404
