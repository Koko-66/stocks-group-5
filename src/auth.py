from flask import Flask, Blueprint, render_template, request, redirect, session, url_for
import re

#importing database
from src.database import User, db

auth = Blueprint("auth", __name__, url_prefix="/auth")

#handling login page
@auth.route('/login', methods=['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            session['loggedin'] = True
            session['user_id'] = user.id
            session['username'] = user.username
            session['email'] = user.email
            message = 'Logged in successfully!'
            return redirect(f'../profile/{user.username}')
        else:
            message = 'Please enter correct email / password!'
    return render_template('login.html', message=message)

#logout option
@auth.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('user_id', None)
    session.pop('email', None)
    return redirect(url_for('login'))


#register
@auth.route('/register', methods=['GET', 'POST'])
def register():
    message = ''
    user = ModuleNotFoundError
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            message = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            message = 'Invalid email address!'
        elif not username or not password or not email:
            message = 'Please fill out the form!'
        elif len(password) < 6:
            message= 'Password is too short'
        elif not username.isalnum() or " " in username:
            message = 'Username should be alphanumeric and no spaces are allowed'
        else:
            try:
                new_user = User(username=username, email=email, password=password)
                db.session.add(new_user)
                db.session.commit()
                message = 'Successful registration!'
            except Exception as e:
                message = 'An error occurred while registering: {}'.format(str(e))
                db.session.rollback()
                print('Error: {}'.format(str(e)))
    elif request.method == 'POST':
        message = 'Please fill out the form!'
    return render_template('register.html', message=message, user=user)




# if __name__ == "__main__":
#     app.run()
