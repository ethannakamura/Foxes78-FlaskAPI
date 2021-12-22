from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_migrate import current
# auth routes need to use forms, import those forms
from app.forms import signupForm, signinForm, updateUsernameForm

# imports for working with our User model and signing users up and logins
from app.models import db, User
from flask_login import login_user, logout_user, current_user, login_required
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
                flash('Username or password did not match. Try again.', category='danger')
                return redirect(url_for('auth.signin'))
            # implied else -> the username and the password given matched a user in our database
            login_user(user)
            print(current_user, current_user.__dict__)
            flash(f'Thanks for logging in, {user.username}.', category='info')
            return redirect(url_for('home'))
        else:
            # we have a bad form submission
            flash('Bad form input, try again', category='warning')
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
                flash('Username or email already taken - please try again.', category='warning')
                return redirect(url_for('auth.signup'))
            login_user(new_user)
            flash(f'Thanks for signing up, {new_user.first_name} {new_user.last_name}!', category='info')
            return redirect(url_for('home'))
        else:
            # we have a bad form submission
            flash('Bad form input, try again', category='warning')
            return redirect(url_for('auth.signup'))

    return render_template('signup.html', form=form) # this return works for GET

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', category='info')
    return redirect(url_for('auth.signin'))


# build a route for a user profile page - where they can update their information if they want
@auth.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = updateUsernameForm() # used by both GET and POST
    # if the user submits form
    if request.method == 'POST':
        # validate the form they submitted
        # check their password
        if form.validate_on_submit() and check_password_hash(current_user.password, form.password.data):
            # check if the requested username is available
            if User.query.filter_by(username=form.newusername.data).first():
                flash('Username already taken. Please try a different one.', category='danger')
                return redirect(url_for('auth.profile'))
            else:
                # following 4 lines are what we do if the new username is available
                current_user.username = form.newusername.data # change the current user's username attribute
                db.session.commit() # update the database with that new change
                flash('Your username has been updated!', category='success')
                return redirect(url_for('auth.profile'))
        else:
            flash('Incorrect password- try again.', category='danger')
            return redirect(url_for('auth.profile'))

    return render_template('profile.html', form=form) # GET