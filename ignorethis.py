from flask import Flask, Blueprint, render_template
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    phonenumber = db.Column(db.String(10), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    pronouns = db.Column(db.String(1000))
    gender = db.Column(db.String(1000))
    attraction = db.Column(db.String(1000))
    bio = db.Column(db.String(1000))

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret-key-goes-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'app.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('app.login'))

    login_user(user, remember=remember)
    return redirect(url_for('app.profile'))

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    phonenumber = request.form.get('phonenumber')
    password = request.form.get('password')
    user = User.query.filter_by(email=email).first()

    if user:
        flash('Email address already exists')
        return redirect(url_for('app.signup'))

    new_user = User(email=email, name=name, phonenumber=phonenumber, password=generate_password_hash(password, method='sha256'))
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('app.login'))

@app.route('/update')
def update():
    return render_template('update.html')

@app.route('/update', methods=['POST'])
def update_post():
    email = request.form.get('email')
    password = request.form.get('password')
    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash('Credentials incorrect.  Please try again')
        return redirect(url_for('app.login'))

    user.name = request.form.get('name')
    user.phonenumber = request.form.get('phonenumber')
    user.pronouns = request.form.get('pronouns')
    user.gender = request.form.get('gender')
    user.romance = request.form.get('romance')
    user.bio = request.form.get('bio')
    user.password = request.form.get('password')
    db.session.commit()

    return redirect(url_for('app.profile'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/resources')
def resources():
    return render_template('resources.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/calender')
def calender():
    return render_template('calender.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/profile')
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
@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

@app.errorhandler(404)
def server_error(e):
    return render_template('404.html'), 404
