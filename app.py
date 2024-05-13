import datetime
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect, url_for, session, flash

from user import user

app = Flask(__name__)
app.secret_key = 'your_secret_key'
p = user()
p.username = 'admin'
p.password = '12345'


from users.views import users_blueprint
from pantry.views import pantry_blueprint
from shopping.views import shopping_blueprint


db = SQLAlchemy(app)

app.register_blueprint(users_blueprint, url_prefix='/user')
app.register_blueprint(pantry_blueprint, url_prefix='/pantry')



login = False

used_items = [
    {"name": "Milk", 'calories': 200},
    {"name": "Bread", 'calories': 100},
    {"name": "Apple", 'calories': 60},
    {"name": "Beef", 'calories': 500},
]
used_calories = set()

for item in used_items:
    used_calories.add(item['calories'])
items = [
    {"name": "Milk", "expiry_date": "2024-05-10", 'quantity': '2', 'calories': 200},
    {"name": "jelly", "expiry_date": "2024-05-11", 'quantity': '5', 'calories': 250},
    {"name": "pork", "expiry_date": "2024-05-12", 'quantity': '4', 'calories': 350},
    {"name": "chocolate", "expiry_date": "2024-05-12", 'quantity': '4', 'calories': 360},
    {"name": "Goat Milk", "expiry_date": "2024-05-13", 'quantity': '2', 'calories': 200},
    {"name": "Bread", "expiry_date": "2024-05-12", 'quantity': '2', 'calories': 100},
    {"name": "Apple", "expiry_date": "2024-04-28", 'quantity': '5', 'calories': 60},
    {"name": "Beef", "expiry_date": "2024-06-30", 'quantity': '5', 'calories': 500},
    {"name": "Lamb", "expiry_date": "2024-09-28", 'quantity': '3', 'calories': 450},
    {"name": "Apple juice", "expiry_date": "2024-05-04", 'quantity': '1', 'calories': 150},
]
expiry_dates = set()

for item in items:
    expiry_dates.add(item['expiry_date'])

today = datetime.date.today()

seven_days_later = today + datetime.timedelta(days=7)

soon_to_expire = set()
soon_to_expire_seven = []

expired = set()

# not_yet_expire = set()

for item in items:
    # 将字符串日期转换为datetime.date对象
    expiry_date = datetime.datetime.strptime(item['expiry_date'], "%Y-%m-%d").date()

    # 检查该日期是否在今天和7天后之间
    if expiry_date <= today:
        # 如果是，将物品名称添加到集合中
        expired.add(item['name'])

    # if expiry_date > today:
    # 如果是，将物品名称添加到集合中
    # not_yet_expire.add(item['name'])

not_yet_expire = [item for item in items if
                  datetime.datetime.strptime(item['expiry_date'], "%Y-%m-%d").date() > today]

for item in items:
    # 将字符串日期转换为datetime.date对象
    expiry_date = datetime.datetime.strptime(item['expiry_date'], "%Y-%m-%d").date()

    # 检查该日期是否在今天和7天后之间
    if today <= expiry_date <= seven_days_later:
        # 如果是，将物品名称添加到集合中
        soon_to_expire.add(item['name'])

for item in items:
    # 将字符串日期转换为datetime.date对象
    expiry_date = datetime.datetime.strptime(item['expiry_date'], "%Y-%m-%d").date()

    # 检查该日期是否在今天和7天后之间
    if today <= expiry_date <= seven_days_later:
        soon_to_expire_seven.append({"name": item['name'], "expiry_date": item['expiry_date']})

print(soon_to_expire_seven)
@app.route('/')
def home():
    return render_template('base.html')


@app.route('/base')
def base():
    return render_template('base.html')





@app.route('/main/items', methods=['GET', 'POST'])
def items_view():
    return render_template('main/items.html', items=items, Foodaboutexpired=soon_to_expire,
                           Foodexpired=expired)


@app.route('/main/create_item', methods=['GET', 'POST'])
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
        return render_template('main/create_item.html')


@app.route('/main/baseLogin')
def baseLogin():
    flash('welcome user  ' + p.username)
    return render_template('main/baseLogin.html', username=p.username, Foodaboutexpired=soon_to_expire,
                           Foodexpired=expired, expiry_date=expiry_date, used_calories=used_calories,
                           used_items=used_items, soon_to_expire_seven=soon_to_expire_seven, today=today)


@app.route('/main/information')
def information():
    return render_template('main/information.html', username=p.username)





@app.route('/main/search', methods=['GET', 'POST'])
def search():
    itemtemp = ""  # Initialize the variable to hold the result
    iteminfo = ""
    if request.method == 'POST':
        itemname = request.form['itemname'].strip()  # Get the item name from form input
        for item in items:
            if item['name'].lower() == itemname.lower():  # Case insensitive comparison
                itemtemp = f"item name is {item['name']} expired date is {item['expiry_date']}"
                iteminfo = item['name']
                break
        else:
            itemtemp = "Item not found"  # Set itemtemp to a not found message if the loop completes with no match

    return render_template('main/search.html', itemtemp=itemtemp,
                           iteminfo=iteminfo)  # Pass the result directly to the template


@app.route('/shopping/shopping_list')
def shopping_list():
    return render_template('shopping/shopping_list.html')  # Adjust the template name as necessary


@app.route('/kitchen/recipes')
def recipe_detail():
    return render_template('kitchen/recipes.html')  # Adjust the template name as necessary


@app.route('/kitchen/kitchen_main', methods=['GET'])
def kitchen_main():
    min_calories = request.args.get('min_calories')
    max_calories = request.args.get('max_calories')
    expiry_date = request.args.get('expiry_date')
    not_expired_only = request.args.get('not_expired') == 'on'

    filtered_items = []
    if min_calories or max_calories or expiry_date or not_expired_only:
        filtered_items = [item for item in items if (min_calories is None or item['calories'] >= int(min_calories)) and
                          (max_calories is None or item['calories'] <= int(max_calories)) and
                          (not not_expired_only or (not_expired_only and datetime.datetime.strptime(item['expiry_date'],
                                                                                                    "%Y-%m-%d").date() >= today)) and
                          (expiry_date is None or datetime.datetime.strptime(item['expiry_date'],
                                                                             "%Y-%m-%d").date() <= datetime.datetime.strptime(
                              expiry_date, "%Y-%m-%d").date())]
    return render_template('kitchen/kitchen_main.html', filtered_items=filtered_items, not_yet_expire=not_yet_expire)





if __name__ == '__main__':
    app.run(debug=True)
