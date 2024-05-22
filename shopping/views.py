# View functions for the shopping HTML template
# Authored by Jacob Norman and Yat Nam Chan

from flask import render_template, flash, redirect, url_for, Blueprint, request
from flask_login import current_user, login_required
from datetime import datetime
from app import db, today
from crawler import fetch_food_storage_info
from models import ShoppingList, QuantifiedFoodItem, FoodItem, ShoppingItem, PantryItem
from shopping.forms import AddItemForm, CreateListForm
from shopping.shopping_util import get_storage_duration, create_shopping_list_util,create_shopping_item,remove_shopping_item,mark_shopping_list_as_complete

shopping_blueprint = Blueprint('shopping', __name__, template_folder='templates')


@shopping_blueprint.route('/shopping_list', methods=['GET'])
@login_required
def shopping_list():
    user_shopping_lists = ShoppingList.query.filter_by(user_id=current_user.id).all()
    return render_template('shopping/shopping_list.html', shopping_lists=user_shopping_lists)

# takes user input of a new list name, creates that list then redirects user to a page to add first items to the list
@shopping_blueprint.route('/create_shopping_list', methods=['GET', 'POST'])
@login_required
def create_shopping_list():
    form = CreateListForm()
    if request.method == 'POST' and form.validate_on_submit():
        list_name = form.listName.data
        shopping_list = create_shopping_list_util(current_user.id, list_name)
        flash("Shopping list created", "success")
        return redirect(url_for('shopping.add_items_to_list', list_id=shopping_list.id))
    return render_template('shopping/create_shopping_list.html', form=form)

# view function to add new items to a list when a list is first created
@shopping_blueprint.route('/add_items_to_list/<int:list_id>', methods=['GET', 'POST'])
@login_required
def add_items_to_list(list_id):
    form = AddItemForm()
    shopping_list = ShoppingList.query.get_or_404(list_id)

    if request.method == 'POST' and form.validate_on_submit():
        food_item_name = form.newItem.data
        quantity = form.itemQuantity.data
        units = form.itemUnits.data

        create_shopping_item(list_id,food_item_name,quantity,units)
        flash("Item added to shopping list", "success")
        return redirect(url_for('shopping.add_items_to_list', list_id=list_id))

    shopping_items = ShoppingItem.query.filter_by(list_id=list_id).all()
    return render_template('shopping/add_items_to_list.html', form=form, list_name=shopping_list.list_name,
                           items=shopping_items, list_id=list_id)


@shopping_blueprint.route('/submit_shopping_list', methods=['POST'])
@login_required
def submit_shopping_list():
    # This function might not be necessary anymore since items are added directly in add_items_to_list view.
    flash("Shopping list submitted successfully", "success")
    return redirect(url_for('shopping.shopping_list'))


@shopping_blueprint.route('/shopping_list_detail/<int:list_id>', methods=['GET', 'POST'])
@login_required
def shopping_list_detail(list_id):
    shopping_list = ShoppingList.query.get_or_404(list_id)
    form = AddItemForm()
    if request.method == 'POST' and form.validate_on_submit():
        food_item_name = form.newItem.data
        quantity = form.itemQuantity.data
        units = form.itemUnits.data

        create_shopping_item(list_id, food_item_name, quantity, units)

        flash("Item added to shopping list", "success")
        return redirect(url_for('shopping.shopping_list_detail', list_id=list_id))

    return render_template('shopping/shopping_list_detail.html', form=form, shopping_list=shopping_list)


@shopping_blueprint.route('/delete_list/<int:list_id>', methods=['POST'])
@login_required
def delete_list(list_id):
    shopping_list = ShoppingList.query.get_or_404(list_id)
    if shopping_list.user_id != current_user.id:
        flash('Unauthorized', 'error')
        return redirect(url_for('shopping.shopping_list'))

    for item in shopping_list.shopping_items:
        db.session.delete(item)

    db.session.delete(shopping_list)
    db.session.commit()
    flash('Shopping list deleted', 'success')
    return redirect(url_for('shopping.shopping_list'))


@shopping_blueprint.route('/delete_item/<int:item_id>', methods=['POST'])
@login_required
def delete_item(item_id):
    shopping_item = ShoppingItem.query.get_or_404(item_id)
    shopping_list = ShoppingList.query.get_or_404(shopping_item.list_id)
    if shopping_list.user_id != current_user.id:
        flash('Unauthorized', 'error')
        return redirect(url_for('shopping.shopping_list_detail', list_id=shopping_item.list_id))
    remove_shopping_item(item_id)
    flash('Item deleted from shopping list', 'success')
    print(shopping_item.list_id)
    return redirect(url_for('shopping.shopping_list_detail', list_id=shopping_item.list_id))

# view function that deletes a shopping list then moves all of its contents into the user's pantry
@shopping_blueprint.route('/complete_list/<int:list_id>', methods=['POST'])
@login_required
def complete_list(list_id):
    shopping_list = ShoppingList.query.get_or_404(list_id)
    if shopping_list.user_id != current_user.id:
        flash('Unauthorized', 'error')
        return redirect(url_for('shopping.shopping_list'))
    mark_shopping_list_as_complete(shopping_list)
    flash('Shopping list completed and items moved to pantry', 'success')
    return redirect(url_for('shopping.shopping_list'))
