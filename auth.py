from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user
from run import User
from run import db

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))

    login_user(user, remember=remember)
    return redirect(url_for('master.profile'))

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    phonenumber = request.form.get('phonenumber')
    password = request.form.get('password')
    user = User.query.filter_by(email=email).first()

    if user:
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    new_user = User(email=email, name=name, phonenumber=phonenumber, password=generate_password_hash(password, method='sha256'))
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))

@auth.route('/update')
def update():
    return render_template('update.html')

@auth.route('/update', methods=['POST'])
def update_post():
    email = request.form.get('email')
    password = request.form.get('password')
    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash('Credentials incorrect.  Please try again')
        return redirect(url_for('auth.login'))

    user.name = request.form.get('name')
    user.phonenumber = request.form.get('phonenumber')
    user.pronouns = request.form.get('pronouns')
    user.gender = request.form.get('gender')
    user.romance = request.form.get('romance')
    user.bio = request.form.get('bio')
    user.password = request.form.get('password')
    db.session.commit()

    return redirect(url_for('master.profile'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('master.index'))
