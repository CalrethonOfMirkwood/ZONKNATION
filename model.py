from flask import Flask
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    phonenumber = db.Column(db.String(9), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    pronouns = db.Column(db.String(1000))
    gender = db.Column(db.String(1000))
    attraction = db.Column(db.String(1000))
    bio = db.Column(db.String(1000))

def create_app():
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

    from auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from master import master as master_blueprint
    app.register_blueprint(master_blueprint)

    return app

create_app()
