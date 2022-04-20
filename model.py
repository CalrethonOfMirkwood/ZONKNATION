from flask_login import UserMixin
from __init__ import db

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
