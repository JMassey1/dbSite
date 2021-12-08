from flask import Blueprint, render_template, flash, request
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    loginData = request.form
    return render_template("login.html")


@auth.route('/logout')
def logout():
    return "<p1>Logout Page</p1>"


@auth.route('/sign-up', methods=['GET', 'POST'])
def signUp():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('fname')
        password = request.form.get('password')
        passwordCheck = request.form.get('passwordCheck')

        if password != passwordCheck:
            flash("Passwords do not match", category='error')
        elif len(password) < 6:
            flash("Password must be at least 6 characters", category='error')
        elif len(username) < 3:
            flash("Username must be at least 4 characters", category='error')
        else:
            flash('Account created successfully!', category='success')

    return render_template("signup.html")
