from flask import Blueprint, render_template, request, redirect, url_for, flash

import datetime

from flask_login import login_required

import testingdata

pantry_blueprint = Blueprint('pantry', __name__, template_folder='templates')

print("Template folder:", pantry_blueprint.template_folder)


@pantry_blueprint.route('/items', methods=['GET', 'POST'])
@login_required
def items_view():
    expiry_dates = set()

    for item in testingdata.items:
        expiry_dates.add(item['expiry_date'])

    today = datetime.date.today()

    seven_days_later = today + datetime.timedelta(days=7)
    expired = set()
    soon_to_expire = set()

    for item in testingdata.items:
        # 将字符串日期转换为datetime.date对象
        expiry_date = datetime.datetime.strptime(item['expiry_date'], "%Y-%m-%d").date()

        # 检查该日期是否在今天和7天后之间
        if expiry_date <= today:
            # 如果是，将物品名称添加到集合中
            expired.add(item['name'])

    for item in testingdata.items:
        # 将字符串日期转换为datetime.date对象
        expiry_date = datetime.datetime.strptime(item['expiry_date'], "%Y-%m-%d").date()

        # 检查该日期是否在今天和7天后之间
        if today <= expiry_date <= seven_days_later:
            # 如果是，将物品名称添加到集合中
            soon_to_expire.add(item['name'])
    return render_template('pantry/items.html', items=testingdata.items, Foodaboutexpired=soon_to_expire,
                           Foodexpired=expired)


@pantry_blueprint.route('/create_item', methods=['GET', 'POST'])
@login_required
def create_item():
    if request.method == 'POST':
        # Here, you can process the form data, but since there's no database,
        # we'll just print it to the console or do nothing with it.
        item_name = request.form['name']
        expiry_date = request.form['expiry_date']
        description = request.form['description']

        # Print to console (server logs)
        print(f"Received item: {item_name}, Expiry: {expiry_date}, Description: {description}")

        # Redirect to a new page or back to the form, or display a success message
        return redirect('/main/create_item')  # Redirects back to the form page
    else:
        # Display the form page
        return render_template('pantry/add_food.html')


@pantry_blueprint.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    item_temp = ""  # Initialize the variable to hold the result
    item_info = ""
    if request.method == 'POST':
        item_name = request.form['item_name'].strip()  # Get the item name from form input
        for item in testingdata.items:
            if item['name'].lower() == item_name.lower():  # Case insensitive comparison
                item_temp = f"item name is {item['name']} expired date is {item['expiry_date']}"
                item_info = item['name']
                break
        else:
            item_temp = "Item not found"  # Set itemtemp to a not found message if the loop completes with no match

    return render_template('pantry/search.html', itemtemp=item_temp,
                           iteminfo=item_info)  # Pass the result directly to the template
