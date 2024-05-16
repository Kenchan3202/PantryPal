from flask import Blueprint, Flask, render_template, request, redirect, url_for, session, flash
from flask_login import current_user

import models
from models import *
from shopping.forms import AddItemForm

shopping_blueprint = Blueprint('shopping', __name__, template_folder='templates')
from app import db


@shopping_blueprint.route('/shopping_list', methods=['GET', 'POST'])
def shopping_list():
    form = AddItemForm()

    if form.validate_on_submit():
        food_item = form.newItem.data
        quantity = form.itemQuantity.data
        units = form.newItem.data

        food_id = FoodItem.query.filter_by(name=food_item)
        if not food_id():
            flash("Food item not found in DB")
            return render_template('shopping/shopping_list.html', form=form)
        else:
            newQFI = QuantifiedFoodItem()
            newQFI.food_id = food_id
            newQFI.quantity = quantity
            newQFI.units = units
            q_food_item = models.QuantifiedFoodItem(food_id=newQFI.food_id,
                                                    quantity=newQFI.quantity,
                                                    units=newQFI.units)
            db.session.add(q_food_item)
            db.session.commit()








    return render_template('shopping/shopping_list.html', form=form)  # Adjust the template name as necessary


@shopping_blueprint.route('/complete_shopping', methods=['GET'])
def complete_shopping():
    # Move all items in shopping list field to pantry field then clear shopping list
    print(f"Complete shopping")
    return redirect(url_for('shopping.shopping_list'))


@shopping_blueprint.route('/add_item')
def add_item():
    # query food item entered, if it exists, add it to shopping list field.
    # If it doesn't exist, alert user and give option to add it to DB
    print(f"Add items")
    return render_template('shopping/shopping_list.html')
