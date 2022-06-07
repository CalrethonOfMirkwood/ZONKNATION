from flask import Flask
from flask_login import LoginManager
from important import db, User
from master import master
from auth import auth
from resourcey.app_resources import app_myresources
from commenty.app_comments import app_comments

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

app.register_blueprint(auth)
app.register_blueprint(master)
app.register_blueprint(app_myresources)
app.register_blueprint(app_comments)
