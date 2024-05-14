from flask import Blueprint, render_template, flash
from flask_login import login_required, current_user


admin_blueprint = Blueprint('admin', __name__, template_folder='templates')

@admin_blueprint.route('/admin')
def admin():
    return render_template('admin/admin.html', name=current_user.firstname)

# view all registered users
@admin_blueprint.route('/view_all_users', methods=['POST'])
@login_required
def view_all_users():

    return render_template('admin/admin.html', name=current_user)



# views all user activities
@admin_blueprint.route('/view_user_activity', methods=['POST'])
@login_required
def view_user_activity():
    return render_template('admin/admin.html')