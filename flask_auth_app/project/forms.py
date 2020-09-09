from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from .models import User, Password
import re
import email_validator

class SignupForm(FlaskForm):
	name = StringField('Name', validators=[DataRequired(), Length(max=10, message=('max length for name is 10'))])
	email = StringField('Email', validators=[DataRequired(), Email(message=('Not a valid email address'))])
	password = PasswordField('Password', validators=[DataRequired()])
	address = StringField('Address')
	phone = StringField('Phone')
	submit = SubmitField()

	def validate_name(self, name):
		user = User.query.filter_by(name=name.data).first()
		if user is not None:
			raise ValidationError('Please use a different username')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user is not None:
			raise ValidationError('Please use a different email')

	def validate_password(self, password):
		while True:
			if re.search('[0-9]',password) is None:
				raise ValidationError('Make sure your password has a number in it')
			elif re.search('[A-Z]',password) is None:
				raise ValidationError('Make sure your password has a capital letter in it')
			elif re.search('[_,$,@,#,!,&,*,]', password) is None:
				raise ValidationError('Make sure your password has a special character')
			else:
				break



