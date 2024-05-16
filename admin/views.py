from flask import Blueprint, render_template, flash, abort
from flask_login import login_required, current_user

admin_blueprint = Blueprint('admin', __name__, template_folder='templates')
from app import app, db
from models import User


@admin_blueprint.route('/admin')
@login_required
def admin():
    if current_user.role != 'admin':
        abort(403)
    return render_template('admin/admin.html', name=current_user.first_name)


# view all registered users
@admin_blueprint.route('/view_all_users')
@login_required
def view_all_users():
    current_users = User.query.filter_by(role='user').all()

    return render_template('admin/admin.html', name=current_user.first_name, current_users=current_users)


@admin_blueprint.route('/view_user_activity')
@login_required
def view_user_activity():
    if current_user.role != 'admin':
        abort(403)

    # Fetch user activities from the database
    users = User.query.all()
    user_activities = [
        {
            'id': user.id,
            'email': user.email,
            'current_login_ip': user.current_login_ip,
            'last_login_ip': user.last_login_ip,
            'total_logins': user.total_logins,
            'registration_date': user.registered_on.strftime(
                "%Y-%m-%d %H:%M:%S") if user.registered_on else 'N/A',
            'last_login': user.last_login.strftime("%Y-%m-%d %H:%M:%S") if user.last_login else 'N/A',
            'current_login': user.current_login.strftime("%Y-%m-%d %H:%M:%S") if user.current_login else 'N/A'
        }
        for user in users
    ]

    return render_template('admin/admin.html', first_name=current_user.first_name, last_name=current_user.last_name,
                           user_activities=user_activities)


@admin_blueprint.route('/logs')
@login_required
def logs():
    if current_user.role != 'admin':
        abort(403)
    with open("app.log", "r") as f:
        content = f.read().splitlines()[-10:]
        content.reverse()

    return render_template('admin/admin.html', logs=content, name=current_user.first_name)
