from flask import Blueprint, render_template, request, flash, redirect, url_for
from . models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, current_user, logout_user

auth = Blueprint("auth", __name__)

@auth.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')
    return render_template("login.html", user = current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Account With that Email Already Exists !', category='error')
        elif password != confirm_password:
            flash("Passwords Don't match!", category="error")
        else:
            new_user = User(email = email, password = generate_password_hash(password, method = "SHA256"))
            db.session.add(new_user)
            db.session.commit()

            login_user(new_user, remember=True)
            flash("Account Created Successfully !", category="success")
            return redirect(url_for('views.home'))

        
    return render_template("register.html", user = current_user)
