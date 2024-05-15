# users/views.py
from datetime import datetime

from cryptography.fernet import Fernet
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from user import user
# from app import app

users_blueprint = Blueprint('users', __name__, template_folder='templates')
from app import app, db
from models import User
p = user()


p.username = 'admin'
p.password = '12345'

# def encrypt(data):
#     cipher_suite = Fernet(app.config['ENCRYPTION_KEY'])
#     return cipher_suite.encrypt(data.encode()).decode()
#
# def decrypt(data):
#     cipher_suite = Fernet(app.config['ENCRYPTION_KEY'])
#     return cipher_suite.decrypt(data.encode()).decode()


@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    # pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        dob = request.form['dob']

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered.')
            return redirect(url_for('users.register'))

        # Validation conditions
        if len(first_name) < 2:
            flash('firstname must be at least 2 characters long')
            return redirect(url_for('user.register'))
        if len(last_name) < 2:
            flash('firstname must be at least 2 characters long')
            return redirect(url_for('user.register'))
        # if re.match(pattern, email):
        #     flash('your email address is wrong')
        #     return redirect(url_for('user.register'))
        if len(password) < 8 or not any(char.isdigit() for char in password) or not any(
                char.isupper() for char in password) or not any(char.islower() for char in password):
            flash(
                'Password must be at least 8 characters long, include an uppercase letter, a lowercase letter, '
                'and a number')
            return redirect(url_for('users.register'))
        if password != confirm_password:
            flash('Passwords do not match')
            return redirect(url_for('users.register'))
        with app.app_context():
            new_user = User(email=email, password=password, first_name=first_name, last_name=last_name, dob=dob)

            db.session.add(new_user)
            db.session.commit()


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
        email = request.form['email']
        password = request.form['password']

        # 从数据库中查找用户
        u1 = User.query.filter_by(email=email).first()

        # 如果找到用户，并且密码匹配
        if u1 and u1.verify_password(password):
            session['logged_in'] = True
            flash('Login successful.')
            return redirect(url_for('baseLogin'))  # 确保这是正确的重定向目标
        else:
            flash('Login failed. Please check your email and password.', 'error')
            return redirect(url_for('users.login'))

    return render_template('user/login.html')
# @users_blueprint.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         email = request.form['email']
#         password = request.form['password']
#
#         if p.password == password:
#             session['logged_in'] = True
#             flash('Login successful.')
#             return redirect(url_for('baseLogin'))
#         else:
#             flash('Login failed. Please check your username and password.', 'error')
#             return redirect(url_for('users.login'))
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
