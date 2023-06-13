from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from .models import User, Role
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=['GET', 'POST'])
def login():
    admin_email = "admin@gmail.com"
    admin_pwd = "admin"
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        professor_validation = None
        try :
            professor_validation = user.professor_token
        except:
            pass
        if admin_email in email and admin_pwd in password:
            login_user(user, remember=True)
            return redirect(url_for("views.admin"))
        if user:
            if check_password_hash(user.password, password):
                if professor_validation:
                    flash("Logged in as Professor!", category="success")
                    login_user(user, remember=True)
                    return redirect(url_for("views.home"))
                else:
                    flash("Logged in as Student!", category="success")
                    login_user(user, remember=True)
                    return redirect(url_for("views.home"))
            else:
                flash("Password is incorrect.", category="error")
        else:
            flash("Email does not exist", category="error")
    return render_template("auth/login.html", user=current_user)

@auth.route("/sign-up", methods=['GET', 'POST'])
def sign_up():
    professor_token_valid = ['123','234', '345']
    if request.method == 'POST':
        email = request.form.get("email")
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        role = request.form.get("role")
        professor_token = str(request.form.get("professor_token"))
        email_exist = User.query.filter_by(email=email).first()
        username_exist = User.query.filter_by(username=username).first()
        professor_token_used = User.query.filter_by(professor_token=professor_token).first()

        if email_exist:
            flash('Email is already in use', category='error')
        elif username_exist:
            flash('Username is already in use', category='error')
        elif password1 != password2:
            flash('Password don\'t match', category='error')
        elif len(username) < 2:
            flash('Username is too short', category='error')
        elif len(password1) < 2:
            flash('Password is too short', category='error')
        elif len(email) < 5:
            flash('Email is invalid', category='error')
        elif professor_token in professor_token_valid:
            if professor_token_used:
                flash('Professor token already used', category='error')
            else:
                new_user = User(email=email, username=username, password=generate_password_hash(password1), professor_token=professor_token)
                db.session.add(new_user)
                db.session.commit()

                new_role = Role(user_id=new_user.id, role=role)
                db.session.add(new_role)
                db.session.commit()

                login_user(new_user, remember=True)
                flash("User Created as Professor!")
                return redirect(url_for('views.home'))
        else:
            new_user = User(email=email, username=username, password=generate_password_hash(password1))
            db.session.add(new_user)
            db.session.commit()
            
            new_role = Role(user_id=new_user.id, role=role)
            db.session.add(new_role)
            db.session.commit()

            login_user(new_user, remember=True)
            flash("User Created as Student!")

            return redirect(url_for('views.home'))

    return render_template("auth/signup.html", user=current_user)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("views.home"))
