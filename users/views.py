# users/views.py
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from users.forms import RegisterForm, LoginForm, ChangePasswordForm
from flask_login import login_user, logout_user, login_required, current_user


users_blueprint = Blueprint('users', __name__, template_folder='templates')
from app import app, db
from models import User


@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    # create signup form object
    form1 = RegisterForm()

    # if request method is POST or form is valid
    if form1.validate_on_submit():
        with app.app_context():
            u1 = User.query.filter_by(email=form1.email.data).first()
        # if this returns a user, then the email already exists in database

        # if email already exists redirect user back to signup page with error message so user can try again
        if u1:
            flash('Email address already exists')
            return render_template('user/register.html', form=form1)

        # create a new user with the form data
        new_user = User(email=form1.email.data,
                        dob=form1.dob.data,
                        first_name=form1.first_name.data,
                        last_name=form1.last_name.data,
                        password=form1.password.data,
                        role='user'
                        )

        # add the new user to the database

        db.session.add(new_user)
        db.session.commit()

        # sends user to login page
        return redirect(url_for('users.login'))
    # if request method is GET or form not valid re-render signup page
    return render_template('user/register.html', form=form1)

# @users_blueprint.route('/register', methods=['GET', 'POST'])
# def register():
#     # pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
#     if request.method == 'POST':
#         email = request.form['email']
#         password = request.form['password']
#         confirm_password = request.form['confirm_password']
#         first_name = request.form['first_name']
#         last_name = request.form['last_name']
#         dob = request.form['dob']
#
#         existing_user = User.query.filter_by(email=email).first()
#         if existing_user:
#             flash('Email already registered.')
#             return redirect(url_for('users.register'))
#
#         # Validation conditions
#         if len(first_name) < 2:
#             flash('firstname must be at least 2 characters long')
#             return redirect(url_for('user.register'))
#         if len(last_name) < 2:
#             flash('firstname must be at least 2 characters long')
#             return redirect(url_for('user.register'))
#         # if re.match(pattern, email):
#         #     flash('your email address is wrong')
#         #     return redirect(url_for('user.register'))
#         if len(password) < 8 or not any(char.isdigit() for char in password) or not any(
#                 char.isupper() for char in password) or not any(char.islower() for char in password):
#             flash(
#                 'Password must be at least 8 characters long, include an uppercase letter, a lowercase letter, '
#                 'and a number')
#             return redirect(url_for('users.register'))
#         if password != confirm_password:
#             flash('Passwords do not match')
#             return redirect(url_for('users.register'))
#         with app.app_context():
#             new_user = User(email=email, password=password, first_name=first_name, last_name=last_name, dob=dob)
#
#             db.session.add(new_user)
#             db.session.commit()
#
#
#         flash('Registration successful.')
#         return redirect(url_for('users.login'))
#     return render_template('user/register.html')

@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.verify_password(form.password.data):
            login_user(user)
            session['logged_in'] = True
            session['user_id'] = user.id
            flash('You have been logged in.', 'success')
            return redirect(url_for('baseLogin'))
        else:
            flash('Invalid email or password.', 'danger')

    return render_template('user/login.html', form=form)

# @users_blueprint.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         email = request.form['email']
#         password = request.form['password']
#
#         # 从数据库中查找用户
#         u1 = User.query.filter_by(email=email).first()
#
#         # 如果找到用户，并且密码匹配
#         if u1 and u1.verify_password(password):
#             session['logged_in'] = True
#             flash('Login successful.')
#             return redirect(url_for('baseLogin'))  # 确保这是正确的重定向目标
#         else:
#             flash('Login failed. Please check your email and password.', 'error')
#             return redirect(url_for('users.login'))
#
#     return render_template('user/login.html')


@users_blueprint.route('/update_password', methods=['GET', 'POST'])
@login_required
def update_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        user = current_user
        if user.verify_password(form.current_password.data):
            if form.new_password.data != form.current_password.data:
                user.set_password(form.new_password.data)
                db.session.commit()
                flash('Your password has been updated.', 'success')
                return redirect(url_for('users.login'))
            else:
                flash('New password cannot be the same as the current password.', 'error')
        else:
            flash('Current password is incorrect.', 'error')
    return render_template('user/update_password.html', form=form)
# @users_blueprint.route('/update_password', methods=['GET', 'POST'])
# def reset_password():
#     if request.method == 'POST':
#         new_password = request.form['new_password']
#         p.password = new_password
#         # flash('Your password has been reset successfully.', 'success')
#         return redirect(url_for('base'))
#     return render_template('user/update_password.html')


@users_blueprint.route('/my_account')
def information():
    return render_template('user/my_account.html', user=current_user)
