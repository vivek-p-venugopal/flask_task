from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(100), unique=True, nullable=False)
	name = db.Column(db.String(10), nullable=False)
	address = db.Column(db.String(1000))
	phone = db.Column(db.Integer())

class Password(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	salt = db.Column(db.String(1000))
	password = db.Column(db.String(1000), nullable=False)
	status = db.Column(db.Enum('active','inactive'))
