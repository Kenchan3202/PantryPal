from flask import Blueprint, Flask, render_template, request, redirect, url_for, session, flash
from flask_login import current_user
from app import db

import models
from models import *
from shopping.forms import AddItemForm, NewListForm

shopping_blueprint = Blueprint('shopping', __name__, template_folder='templates')



@shopping_blueprint.route('/shopping_list')
def shopping_list():
    shopping_lists = ShoppingList.query.filter_by(user_id=current_user.id)
    return render_template('shopping/shopping_list.html',
                           shopping_lists=shopping_lists)  # Adjust the template name as necessary


@shopping_blueprint.route('/view_list/<int:list_id>')
def view_list(list_id):
    return render_template('shopping/view_list.html')


@shopping_blueprint.route('/delete_list', methods=['POST'])
def delete_list():
    return redirect(url_for('shopping.shopping_list'))


@shopping_blueprint.route('/new_list', methods=['POST'])
def new_list():
    form = NewListForm()
    return render_template('shopping/shopping_list.html', form=form)















'''
@shopping_blueprint.route('/complete_shopping', methods=['GET'])
def complete_shopping():
    # Move all items in shopping list field to pantry field then clear shopping list
    print(f"Complete shopping")
    return redirect(url_for('shopping.shopping_list'))


@shopping_blueprint.route('/add_item',methods = ['POST'])
def add_item():
    # query food item entered, if it exists, add it to shopping list field.
    # If it doesn't exist, alert user and give option to add it to DB
    form = AddItemForm()
    print(form.newItem.data)

    if form.validate_on_submit():
        print("Heya")
        food_item = form.newItem.data
        quantity = form.itemQuantity.data
        units = form.newItem.data
        list_name = form.listName.data

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

            list_id = ShoppingList.query.filter_by(list_name=list_name)
            new_shopping_item = models.ShoppingItem(list_id=list_id,
                                                    qfood_id=q_food_item.id)
            db.session.add(new_shopping_item)
            db.session.commit()


print(f"Add items")




'''
