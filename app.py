import datetime

from flask import Flask, render_template, request, redirect, url_for, session, flash

from user import user

app = Flask(__name__)
app.secret_key = 'your_secret_key'
p = user()
items = [
    {"name": "Milk", "expiry_date": "2024-05-01"},
    {"name": "Bread", "expiry_date": "2024-05-12"},
    {"name": "Apple", "expiry_date": "2024-04-28"},
    {"name": "Beef", "expiry_date": "2024-06-30"},
    {"name": "Lamb", "expiry_date": "2024-09-28"},
    {"name": "Apple juice", "expiry_date": "2024-05-04"},
]
expiry_dates = set()

for item in items:
    expiry_dates.add(item['expiry_date'])

today = datetime.date.today()

seven_days_later = today + datetime.timedelta(days=7)

soon_to_expire = set()

expired = set()

for item in items:
    # 将字符串日期转换为datetime.date对象
    expiry_date = datetime.datetime.strptime(item['expiry_date'], "%Y-%m-%d").date()

    # 检查该日期是否在今天和7天后之间
    if expiry_date <= today:
        # 如果是，将物品名称添加到集合中
        expired.add(item['name'])

for item in items:
    # 将字符串日期转换为datetime.date对象
    expiry_date = datetime.datetime.strptime(item['expiry_date'], "%Y-%m-%d").date()

    # 检查该日期是否在今天和7天后之间
    if today <= expiry_date <= seven_days_later:
        # 如果是，将物品名称添加到集合中
        soon_to_expire.add(item['name'])


@app.route('/')
def home():
    return render_template('user/base.html')


@app.route('/base')
def base():
    return render_template('user/base.html')


@app.route('/user/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == p.username and password == p.password:
            session['logged_in'] = True
            return redirect(url_for('baseLogin'))
        else:
            flash('Login failed. Please check your username and password.', 'error')  # 添加错误消息
            return redirect(url_for('login'))
    return render_template('user/login.html')


@app.route('/user/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Passwords do not match')
            return redirect(url_for('register'))

        p.username = username
        p.password = password
        return redirect(url_for('base'))
    return render_template('user/register.html')


@app.route('/main/Items', methods=['GET', 'POST'])
def Items():
    return render_template('main/Items.html', items=items, Foodaboutexpired=soon_to_expire,
                           Foodexpired=expired)


@app.route('/main/baseLogin')
def baseLogin():
    flash('welcome user  ' + p.username)

    return render_template('main/baseLogin.html', username=p.username, Foodaboutexpired=soon_to_expire,
                           Foodexpired=expired)


@app.route('/main/information')
def information():
    return render_template('main/information.html', username=p.username)


@app.route('/main/resetpassword', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        new_password = request.form['new_password']
        p.password = new_password  # 更新密码
        # flash('Your password has been reset successfully.', 'success')
        return redirect(url_for('/user/base'))  # 可以重定向到登录页面或其他页面
    return render_template('main/resetpassword.html')


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

    return render_template('main/search.html', itemtemp=itemtemp, iteminfo=iteminfo)  # Pass the result directly to the template


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=9000, debug=True)
