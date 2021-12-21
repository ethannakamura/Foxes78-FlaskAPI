from flask import Blueprint, render_template, request, redirect, url_for
# auth routes need to use forms, import those forms
from app.forms import signupForm, signinForm

# imports for working with our User model and signing users up and logins
from app.models import db, User
from flask_login import login_user, logout_user, current_user
from werkzeug.security import check_password_hash

auth = Blueprint('auth', __name__, template_folder='auth_templates', url_prefix='/auth')

@auth.route('/signin', methods=['GET', 'POST'])
def signin():
    form = signinForm() # used by both GET and POST

    if request.method == 'POST':
        if form.validate_on_submit():
            print('This user is ready to be checked if they gave the right username and password')
            print(form.username.data, form.password.data)
            user = User.query.filter_by(username=form.username.data).first()
            if user is None or not check_password_hash(user.password, form.password.data):
                # username didn't exist or user gave us the wrong password
                print('bad login attempt')
                return redirect(url_for('auth.signin'))
            # implied else -> the username and the password given matched a user in our database
            login_user(user)
            print(f'Thanks for logging in, {user.username}.')
            return redirect(url_for('home'))
        else:
            # we have a bad form submission
            print('Bad form input, try again')
            return redirect(url_for('auth.signin'))

    return render_template('signin.html', form=form) # works with GET requests

@auth.route('/register', methods=['GET', 'POST'])
def signup():
    # plan to use the signupForm here
    form = signupForm()

    # 2 scenarios
        # GET - just render the template for the user
        # POST - take in the submitted form info and do something with it
    if request.method == 'POST': # if the user submitted the form
        # ok, the user is trying to send us form info
        # validate the form info
        if form.validate_on_submit():
            # we have proper user info - we want to create a user account
            print('successful new user data received')
            new_user = User(form.username.data, form.email.data, form.password.data, form.first_name.data, form.last_name.data)        
            print(f'New user created - {new_user.__dict__}')
            # try to upload that user to our database
            #   now 2 things could go wrong - we said that username and email must be unique - if either is not unique, we get an error
            try:
                db.session.add(new_user)
                db.session.commit()
            except:
                print('Username or email taken.')
                return redirect(url_for('auth.signup'))
            print('New user registered!')
            login_user(new_user)
            return redirect(url_for('home'))
        else:
            # we have a bad form submission
            print('Bad form input, try again')
            return redirect(url_for('auth.signup'))

    return render_template('signup.html', form=form) # this return works for GET


@auth.route('/logout')
def logout():
    logout_user()
    print('Logged out.')
    return redirect(url_for('auth.signin'))