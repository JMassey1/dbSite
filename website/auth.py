from . import engine, session, User
from flask import Blueprint, render_template, flash, request, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import create_engine, table, column, select, update, insert, text

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        with engine.connect() as conn:
            user = session.query(User).filter_by(username = username).first()
            if user:
                if check_password_hash(user.password, password):
                    flash('Logged in!', category='success')
                    login_user(user, remember=True)
                    return redirect(url_for('views.home'))
                else:
                    flash('Incorrect password, try again.', category='error')
            else:
                flash('User not found, try again.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def signUp():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        passwordCheck = request.form.get('passwordCheck')
        userType = request.form['userType']

        with engine.connect() as conn:
            userExists = conn.execute(
                text("SELECT COUNT(1) FROM Users WHERE username = :username"),
                {"username": username}
            )

            if userExists.first()[0] == 1:
                flash("Username already exists, please choose a different username", category='error')
            elif password != passwordCheck:
                flash("Passwords do not match", category='error')
            elif len(password) < 6:
                flash("Password must be at least 6 characters", category='error')
            elif len(username) < 3:
                flash("Username must be at least 4 characters", category='error')
            else:
                # Add user here
                # password = generate_password_hash(password)
                flash('Account created successfully!', category='success')
                result = conn.execute(
                    text("INSERT INTO Users (username, email, password) VALUES (:username, :email, :password)"),
                    [{"username": username, "email": email, "password": generate_password_hash(password)}]
                )
                if (userType == "listener"):
                    result = conn.execute(
                        text("INSERT INTO Listeners (User_ID) SELECT User_ID FROM Users WHERE username = :username"),
                        {"username": username}
                    )
                if (userType == "artist"):
                    result = conn.execute(
                        text("INSERT INTO Artists (User_ID) SELECT User_ID FROM Users WHERE username = :username"),
                        {"username": username}
                    )

                return(redirect(url_for('views.home')))
    return render_template("signup.html", user=current_user)