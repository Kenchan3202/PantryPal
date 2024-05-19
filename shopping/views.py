from flask import render_template, flash, redirect, url_for, Blueprint, request, jsonify, session
from flask_login import current_user, login_required

from app import db
from models import ShoppingList, QuantifiedFoodItem, FoodItem, ShoppingItem, PantryItem
from shopping.forms import AddItemForm, CreateListForm

shopping_blueprint = Blueprint('shopping', __name__, template_folder='templates')

@shopping_blueprint.route('/shopping_list', methods=['GET'])
@login_required
def shopping_list():
    user_shopping_lists = ShoppingList.query.filter_by(user_id=current_user.id).all()
    return render_template('shopping/shopping_list.html', shopping_lists=user_shopping_lists)

@shopping_blueprint.route('/create_shopping_list', methods=['GET', 'POST'])
@login_required
def create_shopping_list():
    form = CreateListForm()
    if request.method == 'POST' and form.validate_on_submit():
        list_name = form.listName.data
        session['list_name'] = list_name
        session['shopping_items'] = []
        return redirect(url_for('shopping.add_items_to_list'))
    return render_template('shopping/create_shopping_list.html', form=form)

@shopping_blueprint.route('/add_items_to_list', methods=['GET', 'POST'])
@login_required
def add_items_to_list():
    form = AddItemForm()
    if 'list_name' not in session:
        return redirect(url_for('shopping.create_shopping_list'))

    if request.method == 'POST' and form.validate_on_submit():
        food_item_name = form.newItem.data
        quantity = form.itemQuantity.data
        units = form.itemUnits.data

        food = FoodItem.query.filter_by(name=food_item_name).first()
        if not food:
            flash("Food item not found in DB", "error")
        else:
            shopping_item = {
                'food_id': food.id,
                'quantity': quantity,
                'units': units
            }
            session['shopping_items'].append(shopping_item)
            flash("Item added to shopping list", "success")
            return redirect(url_for('shopping.add_items_to_list'))

    return render_template('shopping/add_items_to_list.html', form=form, list_name=session['list_name'], items=session['shopping_items'])

@shopping_blueprint.route('/submit_shopping_list', methods=['POST'])
@login_required
def submit_shopping_list():
    if 'list_name' not in session or 'shopping_items' not in session:
        return redirect(url_for('shopping.create_shopping_list'))

    shopping_list = ShoppingList(user_id=current_user.id, list_name=session['list_name'])
    db.session.add(shopping_list)
    db.session.commit()

    for item in session['shopping_items']:
        newQFI = QuantifiedFoodItem(food_id=item['food_id'], quantity=item['quantity'], units=item['units'])
        db.session.add(newQFI)
        db.session.commit()

        new_shopping_item = ShoppingItem(list_id=shopping_list.id, qfood_id=newQFI.id)
        db.session.add(new_shopping_item)
        db.session.commit()

    session.pop('list_name', None)
    session.pop('shopping_items', None)
    flash("Shopping list created successfully", "success")
    return redirect(url_for('shopping.shopping_list'))

@shopping_blueprint.route('/shopping_list_detail/<int:list_id>', methods=['GET', 'POST'])
@login_required
def shopping_list_detail(list_id):
    shopping_list = ShoppingList.query.get_or_404(list_id)
    form = AddItemForm()
    if request.method == 'POST' and form.validate_on_submit():
        if shopping_list and shopping_list.user_id == current_user.id:
            food_item_name = form.newItem.data
            quantity = form.itemQuantity.data
            units = form.itemUnits.data

            food = FoodItem.query.filter_by(name=food_item_name).first()
            if not food:
                flash("Food item not found in DB", "error")
            else:
                newQFI = QuantifiedFoodItem(food_id=food.id, quantity=quantity, units=units)
                db.session.add(newQFI)
                db.session.commit()

                new_shopping_item = ShoppingItem(list_id=shopping_list.id, qfood_id=newQFI.id)
                db.session.add(new_shopping_item)
                db.session.commit()
                flash("Item added to shopping list", "success")
        else:
            flash("Shopping list not found or unauthorized", "error")
        return redirect(url_for('shopping.shopping_list_detail', list_id=list_id))
    return render_template('shopping/shopping_list_detail.html', form=form, shopping_list=shopping_list)

@shopping_blueprint.route('/delete_list/<int:list_id>', methods=['POST'])
@login_required
def delete_list(list_id):
    shopping_list = ShoppingList.query.get_or_404(list_id)
    if shopping_list.user_id != current_user.id:
        flash('Unauthorized', 'error')
        return redirect(url_for('shopping.shopping_list'))
    db.session.delete(shopping_list)
    db.session.commit()
    flash('Shopping list deleted', 'success')
    return redirect(url_for('shopping.shopping_list'))

@shopping_blueprint.route('/delete_item/<int:item_id>', methods=['POST'])
@login_required
def delete_item(item_id):
    shopping_item = ShoppingItem.query.get_or_404(item_id)
    if shopping_item.shoppinglist.user_id != current_user.id:
        flash('Unauthorized', 'error')
        return redirect(url_for('shopping.shopping_list_detail', list_id=shopping_item.shoppinglist.id))
    db.session.delete(shopping_item)
    db.session.commit()
    flash('Item deleted from shopping list', 'success')
    return redirect(url_for('shopping.shopping_list_detail', list_id=shopping_item.shoppinglist.id))

@shopping_blueprint.route('/complete_list/<int:list_id>', methods=['POST'])
@login_required
def complete_list(list_id):
    shopping_list = ShoppingList.query.get_or_404(list_id)
    if shopping_list.user_id != current_user.id:
        flash('Unauthorized', 'error')
        return redirect(url_for('shopping.shopping_list'))
    for item in shopping_list.shopping_items:
        pantry_item = PantryItem(user_id=current_user.id, qfood_id=item.qfood_id, expiry=None, calories=0)
        db.session.add(pantry_item)
        db.session.delete(item)
    db.session.commit()
    flash('Shopping list completed and items moved to pantry', 'success')
    return redirect(url_for('shopping.shopping_list'))




