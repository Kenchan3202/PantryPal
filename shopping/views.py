from flask import Blueprint, Flask, render_template, request, redirect, url_for, session, flash

shopping_blueprint = Blueprint('shopping', __name__, template_folder='templates')


@shopping_blueprint.route('/shopping_list')
def shopping_list():
    return render_template('shopping/shopping_list.html')  # Adjust the template name as necessary


@shopping_blueprint.route('/complete_shopping')
def complete_shopping():
    print(f"Complete shopping")
    return render_template('shopping/shopping_list.html')


@shopping_blueprint.route('/add_item')
def add_item():
    print(f"Add items")
    return render_template('shopping/shopping_list.html')
