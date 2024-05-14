# users/views.py
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from flask_login import LoginManager
from werkzeug.security import generate_password_hash, check_password_hash

from app import app, db
from user import user

users_blueprint = Blueprint('users', __name__, template_folder='templates')

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = 'users.login'

p = user()
#p.username = 'admin'
#p.password = '12345'

@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Validation conditions
        if len(username) < 3:
            flash('Username must be at least 3 characters long')
            return redirect(url_for('user.register'))
        if len(password) < 8 or not any(char.isdigit() for char in password) or not any(
                char.isupper() for char in password) or not any(char.islower() for char in password):
            flash(
                'Password must be at least 8 characters long, include an uppercase letter, a lowercase letter, '
                'and a number')
            return redirect(url_for('users.register'))
        if password != confirm_password:
            flash('Passwords do not match')
            return redirect(url_for('users.register'))

        # Hash the password
        hashed_password = generate_password_hash(password)
        print(p.password)
        # Here you would normally save the username and hashed_password to a database
        # Assuming user object has an attribute for password storage
        p.password = hashed_password  # Saving hashed password instead of plain one
        print(p.password)
        flash('Registration successful.')
        return redirect(url_for('users.login'))
    return render_template('user/register.html')

# def register():
#     if request.method == 'POST':
#         email = request.form['email']
#         password = request.form['password']
#         confirm_password = request.form['confirm_password']
#         first_name = request.form['first_name']
#         last_name = request.form['last_name']
#         dob = request.form['dob']
#
#         if password != confirm_password:
#             flash('Passwords do not match.')
#             return redirect(url_for('users.register'))
#
#         hashed_password = generate_password_hash(password)
#
#         # 创建新用户
#         new_user = User(email=email, password=hashed_password, first_name=first_name, last_name=last_name, dob=dob)
#         db.session.add(new_user)
#         try:
#             db.session.commit()
#             flash('Registration successful.')
#             return redirect(url_for('users.login'))
#         except Exception as e:
#             db.session.rollback()
#             flash('Error: ' + str(e))
#             return redirect(url_for('users.register'))
#
#     return render_template('user/register.html')

@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if user and check_password_hash(p.password, password):
            session['logged_in'] = True
            flash('Login successful.')
            return redirect(url_for('baseLogin'))
        else:
            flash('Login failed. Please check your username and password.', 'error')
            return redirect(url_for('users.login'))
    return render_template('user/login.html')
# @users_blueprint.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         email = request.form['email']
#         password = request.form['password']
#
#         user = User.query.filter_by(email=email).first()
#
#         if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
#             session['logged_in'] = True
#             flash('Login successful.')
#             return redirect(url_for('main.dashboard'))  # 修改为适合的视图函数
#         else:
#             flash('Invalid username or password.')
#             return redirect(url_for('users.login'))
#
#     return render_template('user/login.html')




@users_blueprint.route('/update_password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        new_password = request.form['new_password']
        p.password = new_password
        # flash('Your password has been reset successfully.', 'success')
        return redirect(url_for('base'))
    return render_template('user/update_password.html')


@users_blueprint.route('/information')
def information():
    return render_template('user/information.html', username=p.username)
