from flask import Blueprint, Flask, render_template, request, redirect, url_for, session, flash

import app

from user import user

shopping_blueprint = Blueprint('shopping', __name__, template_folder='templates')
@app.route('/shopping/shopping_list')
def shopping_list():
    return render_template('shopping/shopping_list.html')  # Adjust the template name as necessary
