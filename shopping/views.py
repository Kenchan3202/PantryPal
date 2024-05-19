from flask import Blueprint, Flask, render_template, request, redirect, url_for, session, flash
from flask_login import current_user, login_required

import models
from models import *
from shopping.forms import AddItemForm

shopping_blueprint = Blueprint('shopping', __name__, template_folder='templates')
from app import db


@shopping_blueprint.route('/shopping_list', methods=['GET', 'POST'])
@login_required
def shopping_list():
    form = AddItemForm()
    if form.validate_on_submit():
        food_item = form.newItem.data
        quantity = form.itemQuantity.data
        units = form.itemUnits.data
        list_name = form.listName.data

        food_id = FoodItem.query.filter_by(name=food_item).first()
        if not food_id:
            flash("Food item not found in DB", "error")
            return render_template('shopping/shopping_list.html', form=form)
        else:
            newQFI = QuantifiedFoodItem(food_id=food_id.id, quantity=quantity, units=units)
            db.session.add(newQFI)
            db.session.commit()

            list_id = ShoppingList.query.filter_by(list_name=list_name).first()
            if not list_id:
                list_id = ShoppingList(user_id=current_user.id, list_name=list_name)
                db.session.add(list_id)
                db.session.flush()

            new_shopping_item = ShoppingItem(list_id=list_id.id, qfood_id=newQFI.id)
            db.session.add(new_shopping_item)
            db.session.commit()
            flash("Item added successfully", "success")

    return render_template('shopping/shopping_list.html', form=form)


@shopping_blueprint.route('/complete_shopping', methods=['GET'])
@login_required
def complete_shopping():
    # Move all items in shopping list field to pantry field then clear shopping list
    print(f"Complete shopping")
    return redirect(url_for('shopping.shopping_list'))


@shopping_blueprint.route('/add_item',methods = ['POST'])
def add_item():
    # query food item entered, if it exists, add it to shopping list field.
    # If it doesn't exist, alert user and give option to add it to DB
    print(f"Add items")



    return render_template('shopping/shopping_list.html')
