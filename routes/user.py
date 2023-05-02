from flask import Blueprint, render_template, flash, redirect, url_for, session, g, jsonify, request
from sqlalchemy.exc import IntegrityError

from db import db

from models.user import User
from models.forms import SignupForm, LoginForm

from routes.amada import amada
from routes.punch import punch
from routes.trumpf import trumpf
from routes.forming import forming
from routes.requests import requests
from routes.general import general
from routes.errors import errors
from routes.seed import seed
from routes.documentation import docs
from routes.prototypes import proto

from random import random

from utilities import send_temp_email

current_user_id = 'current_user_id'

user = Blueprint(
    'user',
    __name__,
    static_folder='../static',
    template_folder='../templates/user',
    url_prefix='/user'
)


# # # # # # # # # # # # # # # # # # # #
#                                     #
# User signup and login authorization #
#                                     #
# # # # # # # # # # # # # # # # # # # #

@user.route('/signup', methods=["GET", "POST"])
def signup_page():
    """ Show sign up form - Validate and create user upon success - Reject and redo on failure """

    if current_user_id in session:
        return redirect(url_for('home'))

    form = SignupForm()

    if request.method == "POST":

        temp_password = str(random())[2:8]

        try:
            user = User.signup(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                password=temp_password,
                email=form.email.data.lower()
            )

            db.session.commit()

        except IntegrityError:
            flash("Username/Email already exists", 'danger')
            return render_template('/user/sign_up.html', form=form)

        except Exception as err:
            flash("Unknown error has occurred. Try again later", 'danger')
            print(err)
            return render_template('/user/sign_up.html', form=form)

        flash('Please check your email for your temporary password', "success")
        session['email'] = form.email.data.lower()
        send_temp_email(session["email"], temp_password)
        session["code"] = temp_password
        
        return redirect(url_for('user.check_code'))

    if request.method == "GET":
        return render_template('/user/sign_up.html', form=form)


@user.route('/login', methods=["GET", "POST"])
def login_page():
    """ Show login form """
    
    if current_user_id in session:
        return redirect(url_for('home'))

    if request.method == "GET":
        return render_template('/user/login.html')

    if request.method == "POST":
        email = request.form.get('email').lower()
        
        user = User.authenticate(
            email=email,
            password=request.form.get('password')
        )

        print(request.form)
        

        if user:
            do_login(user)
            session['email'] = email
            flash(f"Hello, {user.first_name}!", "success")

            return redirect(url_for('home'))
        else:
            flash("Invalid Credentials.", "danger")
            return redirect(url_for('user.login_page'))


@user.route('/logout', methods=["GET"])
def logout_user():
    """Initiate Logout"""

    do_logout()
    flash('Successfully signed out', 'success')

    return redirect(url_for('user.login_page'))


@user.route('/verification', methods=["GET", "POST"])
def check_code():
    if request.method == "GET":
        return render_template('/user/verification.html', email=session['email'], code=session['code'])

    if request.method == "POST":

        code = request.form.get('1') + request.form.get('2') + request.form.get(
            '3') + request.form.get('4') + request.form.get('5') + request.form.get('6')

        user = User.authenticate(
            email=session['email'],
            password=code)

        if user:
            return render_template('/user/change_password.html')
        else:
            flash("Invalid verification code. Please try again.", "danger")
            return render_template('/user/verification.html', email=session['email'])


def do_login(user):
    """ Log in user """

    session[current_user_id] = user.id


def do_logout():
    """ Log out current user """

    if current_user_id in session:
        del session[current_user_id]

    g.user = None


@user.route('/change-password', methods=["GET", "POST"])
def change_password():
    if g.user.id == 4:
        return redirect(url_for('home')) # Guest user shouldn't change password
    
    if request.method == "GET":
        return render_template('/user/change_password.html')

    if request.method == "POST":

        user = User.new_password(
            session["email"], request.form.get('password'))

        do_login(user)
        flash(f"Password successfully changed!", "success")
        return redirect(url_for('home'))
