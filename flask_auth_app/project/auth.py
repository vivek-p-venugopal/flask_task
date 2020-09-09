from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, logout_user, login_required
from .models import User, Password
from flask_scrypt import generate_random_salt
import re

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('main.index'))

@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    phone = request.form.get('phone')
    address = request.form.get('address')

    user = User.query.filter_by(email=email).first()

    if user:
    	flash('Email address already exists')
    	return redirect(url_for('auth.signup'))
    if len(name) > 10:
	    flash('Allowed max length of name is 10')
	    return redirect(url_for('auth.signup'))
    while True:
	    if re.search('[0-9]',password) is None:
		    flash('Make sure your password has a number in it')
		    return redirect(url_for('auth.signup'))
	    elif re.search('[A-Z]',password) is None:
		    flash('Make sure your password has a capital letter in it')
		    return redirect(url_for(auth.signup))
	    elif re.search('[@_!#$%^&*()<>?/|]', password) is None:
		    flash('Make sure your password has a special character')
		    return redirect(url_for('auth.signup'))
	    else:
		    break

    new_user = User(email=email, name=name, address=address, phone=phone)    

    db.session.add(new_user)
    db.session.commit()

    salt = generate_random_salt()
    password_full = str(salt) + str(password)
    new_password = Password(user_id=new_user.id, salt=salt, password=generate_password_hash(password_full, method='sha256'))

    db.session.add(new_password)
    db.session.commit()
    return redirect(url_for('auth.login'))

...
@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
	

    user = User.query.filter_by(email=email).first()
    password_object = Password.query.filter_by(user_id=user.id).first()

    password_full = str(password_object.salt) + str(password)
    if not user or not check_password_hash(password_object.password, password_full):
       	flash('Please check your login details and try again.')
       	return redirect(url_for('auth.login'))

    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))