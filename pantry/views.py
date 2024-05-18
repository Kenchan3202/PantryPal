from flask import Blueprint, render_template, request, redirect, url_for, flash

import datetime

from flask_login import login_required, current_user

from app import db
from models import PantryItem, QuantifiedFoodItem, FoodItem

pantry_blueprint = Blueprint('pantry', __name__, template_folder='templates')

print("Template folder:", pantry_blueprint.template_folder)
from app import app


@pantry_blueprint.route('/items', methods=['GET', 'POST'])
@login_required
def items_view():
    user_id = current_user.id
    pantry_items = PantryItem.query.filter_by(user_id=user_id).all()

    today = datetime.date.today()
    seven_days_later = today + datetime.timedelta(days=7)
    expired = set()
    soon_to_expire = set()

    for item in pantry_items:
        # 修改日期格式解析为 'YYYY-MM-DD'
        try:
            expiry_date = datetime.datetime.strptime(item.get_expiry(), "%Y-%m-%d").date()
        except ValueError:
            continue  # 处理错误日期格式

        if expiry_date <= today:
            expired.add(item.get_name())
        elif today <= expiry_date <= seven_days_later:
            soon_to_expire.add(item.get_name())

    return render_template('pantry/items.html', items=pantry_items, Foodaboutexpired=soon_to_expire, Foodexpired=expired)


@pantry_blueprint.route('/create_item', methods=['GET', 'POST'])
@login_required
def create_item():
    if request.method == 'POST':
        item_name = request.form['name']
        expiry_date = request.form['expiry_date']
        quantity = request.form['quantity']
        calories = request.form['calories']

        # 检查食品项是否已存在
        food_item = FoodItem.query.filter_by(name=item_name).first()
        if not food_item:
            # 创建新的食品项
            food_item = FoodItem(food_name=item_name)
            db.session.add(food_item)
            db.session.flush()  # 获取新创建的food_item的ID

        # 创建QuantifiedFoodItem和PantryItem
        q_food_item = QuantifiedFoodItem(food_id=food_item.id, quantity=quantity, units="g")  # 假设单位为g
        db.session.add(q_food_item)
        db.session.flush()  # 获取新创建的q_food_item的ID

        pantry_item = PantryItem(user_id=current_user.id, qfood_id=q_food_item.id, expiry=expiry_date,
                                 calories=calories)
        db.session.add(pantry_item)

        db.session.commit()

        flash('Item successfully added to pantry!', 'success')
        return redirect(url_for('pantry.items_view'))

    return render_template('pantry/add_food.html')


@pantry_blueprint.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    items = []  # Initialize the list to hold the result
    if request.method == 'POST':
        item_name = request.form['itemname'].strip()  # Get the item name from form input
        items = (db.session.query(PantryItem)
                 .join(QuantifiedFoodItem)
                 .join(FoodItem)
                 .filter(FoodItem.name.ilike(f"%{item_name}%"))
                 .filter(PantryItem.user_id == current_user.id)
                 .all())

    return render_template('pantry/search.html', items=items)  # Pass the result directly to the template



@pantry_blueprint.route('/delete_item/<int:item_id>', methods=['POST'])
@login_required
def delete_item(item_id):
    item = PantryItem.query.get_or_404(item_id)
    if item.user_id != current_user.id:
        flash('You do not have permission to delete this item.', 'danger')
        return redirect(url_for('pantry.items_view'))

    db.session.delete(item)
    db.session.commit()
    flash('Item successfully deleted!', 'success')
    return redirect(url_for('pantry.items_view'))
