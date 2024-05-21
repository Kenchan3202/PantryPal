from flask import Blueprint, render_template, request, redirect, url_for, flash

import datetime

from flask_login import login_required, current_user

from app import db
from models import PantryItem, QuantifiedFoodItem, FoodItem

# Initialize pantry blueprint
pantry_blueprint = Blueprint('pantry', __name__, template_folder='templates')

# Debugging to confirm the correct template folder
print("Template folder:", pantry_blueprint.template_folder)


@pantry_blueprint.route('/items', methods=['GET', 'POST'])
@login_required
def items_view():
    user_id = current_user.id

    # Query all pantry items for the current user
    pantry_items = PantryItem.query.filter_by(user_id=user_id).all()

    # Calculate today's date and a date seven days in the future
    today = datetime.date.today()
    seven_days_later = today + datetime.timedelta(days=7)

    # Initialize sets to track expired and soon-to-expire items
    expired = set()
    soon_to_expire = set()

    # Iterate through all pantry items to categorize them by expiry date
    for item in pantry_items:
        try:
            expiry_date = datetime.datetime.strptime(item.get_expiry(), "%Y-%m-%d").date()
        except ValueError:
            continue  # This skips item with invalid date formats

        # Categorize the food items based on their expiry dates
        if expiry_date <= today:
            expired.add(item.get_name())
        elif today <= expiry_date <= seven_days_later:
            soon_to_expire.add(item.get_name())

    # Get filter parameters
    min_calories = request.args.get('min_calories')
    max_calories = request.args.get('max_calories')
    not_expired_only = request.args.get('not_expired') == 'on'

    # Initialize filter items as None
    filtered_items = None

    # Apply filters if any filter parameters are provided
    if min_calories or max_calories or not_expired_only:
        filtered_items = [item for item in pantry_items if
                          (min_calories is None or item.calories >= int(min_calories)) and
                          (max_calories is None or item.calories <= int(max_calories)) and
                          (not not_expired_only or (not_expired_only and datetime.datetime.strptime(item.expiry, "%Y-%m-%d").date() >= today))]

    # Render the template with all items, categorized items, and filtered items (if any)
    return render_template('pantry/items.html', items=pantry_items, Foodaboutexpired=soon_to_expire,
                           Foodexpired=expired, filtered_items=filtered_items)


@pantry_blueprint.route('/create_item', methods=['GET', 'POST'])
@login_required
def create_item():
    # Handle form submission
    if request.method == 'POST':
        item_name = request.form['name']
        expiry_date = request.form['expiry_date']
        quantity = request.form['quantity']
        calories = request.form['calories']

        # Check if the food item already exists in the database
        food_item = FoodItem.query.filter_by(name=item_name).first()
        if not food_item:
            # If the food item does not exist, create a new FoodItem entry
            food_item = FoodItem(food_name=item_name)
            db.session.add(food_item)
            db.session.flush()

        # Create a QuantifiedFoodItem entry for the food item with the given quantity and units
        q_food_item = QuantifiedFoodItem(food_id=food_item.id, quantity=quantity, units="g")
        db.session.add(q_food_item)
        db.session.flush()

        # Create a PantryItem entry linking the user to the quantified food item with expiry date and calories
        pantry_item = PantryItem(user_id=current_user.id, qfood_id=q_food_item.id, expiry=expiry_date,
                                 calories=calories)
        db.session.add(pantry_item)

        db.session.commit()  # Commits all changes to the database

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
    # Retrieve the pantry item by its ID or return a 404 error if not found
    item = PantryItem.query.get_or_404(item_id)

    # Check if the current user is the owner of the item
    if item.user_id != current_user.id:
        # If not, flash an error message and redirect to the pantry items view
        flash('You do not have permission to delete this item.', 'danger')
        return redirect(url_for('pantry.items_view'))

    db.session.delete(item)  # Delete item from the database
    db.session.commit()
    flash('Item successfully deleted!', 'success')
    return redirect(url_for('pantry.items_view'))
