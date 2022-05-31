from flask import Flask, Blueprint, render_template
from flask_login import UserMixin
from __init__ import db
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
@@ -11,3 +15,29 @@ class User(UserMixin, db.Model):
    gender = db.Column(db.String(1000))
    attraction = db.Column(db.String(1000))
    bio = db.Column(db.String(1000))

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret-key-goes-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
return User.query.get(int(user_id))

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

app.register_blueprint(auth_blueprint)


master = Blueprint('master', __name__)

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

app.register_blueprint(master_blueprint)
