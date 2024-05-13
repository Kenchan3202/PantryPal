# users/views.py
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from user import user
from werkzeug.security import generate_password_hash, check_password_hash

users_blueprint = Blueprint('users', __name__, template_folder='templates')

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
        flash('Registration successful.')
        return redirect(url_for('users.login'))
    return render_template('user/register.html')

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
