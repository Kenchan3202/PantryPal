from flask import Blueprint, Flask, render_template, request, redirect, url_for, session, flash


from user import user

shopping_blueprint = Blueprint('shopping', __name__, template_folder='templates')
@shopping_blueprint.route('/shopping_list')
def shopping_list():
    return render_template('shopping/shopping_list.html')  # Adjust the template name as necessary
