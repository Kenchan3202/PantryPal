from flask import Blueprint, Flask, render_template, request, redirect, url_for, session, flash
from models import FoodItem
from app import db
from shopping.forms import AddItemForm

shopping_blueprint = Blueprint('shopping', __name__, template_folder='templates')


@shopping_blueprint.route('/shopping_list', methods=['GET', 'POST'])
def shopping_list():
    form = AddItemForm()



    return render_template('shopping/shopping_list.html', form = form)  # Adjust the template name as necessary


@shopping_blueprint.route('/complete_shopping')
def complete_shopping():
    # Move all items in shopping list field to pantry field then clear shopping list
    print(f"Complete shopping")
    return render_template('shopping/shopping_list.html')


@shopping_blueprint.route('/add_item')
def add_item():
    # query food item entered, if it exists, add it to shopping list field.
    # If it doesn't exist, alert user and give option to add it to DB
    print(f"Add items")
    return render_template('shopping/shopping_list.html')
