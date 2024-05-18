from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from flask_login import login_user, logout_user, login_required, current_user
from users.forms import RegisterForm, LoginForm, ChangePasswordForm
from models import User, PantryItem
from app import db

users_blueprint = Blueprint('users', __name__, template_folder='templates')
from app import app

@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form1 = RegisterForm()
    if form1.validate_on_submit():
        u1 = User.query.filter_by(email=form1.email.data).first()
        if u1:
            flash('Email address already exists')
            return render_template('user/register.html', form=form1)
        new_user = User(
            email=form1.email.data,
            dob=form1.dob.data,
            first_name=form1.first_name.data,
            last_name=form1.last_name.data,
            password=form1.password.data,
            role='user'
        )
        db.session.add(new_user)
        db.session.commit()
        app.logger.info(f"User registered: {form1.email.data}, IP: {request.remote_addr}")
        return redirect(url_for('users.login'))
    return render_template('user/register.html', form=form1)

@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.verify_password(form.password.data):
            login_user(user)
            user.last_login = user.current_login
            user.current_login = datetime.utcnow()
            user.last_login_ip = user.current_login_ip or request.remote_addr
            user.current_login_ip = request.remote_addr
            user.total_logins += 1
            user.update_security_fields_on_login(ip_addr=request.remote_addr)
            db.session.commit()
            session['logged_in'] = True
            session['user_id'] = user.id
            app.logger.info(f"User logged in: {form.email.data}, IP: {request.remote_addr}")
            flash('You have been logged in.', 'success')
            if user.role == 'admin':
                return redirect(url_for('admin.admin'))
            return redirect(url_for('baseLogin'))
        else:
            flash('Invalid email or password.', 'danger')
    return render_template('user/login.html', form=form)

@users_blueprint.route('/my_account')
def information():
    return render_template('user/my_account.html', user=current_user)

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

@users_blueprint.route('/logout')
@login_required
def logout():
    user_info = f"User logged out: {current_user.email}, IP: {request.remote_addr}"
    logout_user()
    session['logged_in'] = False
    app.logger.info(user_info)
    return redirect(url_for('home'))


