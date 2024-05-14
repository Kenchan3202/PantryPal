import datetime
import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

# from user import user

import testingdata

app = Flask(__name__)
app.secret_key = 'your_secret_key'
# p = user()
# p.username = 'admin'
# p.password = '12345'

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['ENCRYPTION_KEY'] = os.getenv('ENCRYPTION_KEY')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['RECAPTCHA_PUBLIC_KEY'] = os.getenv('RECAPTCHA_PUBLIC_KEY')
app.config['RECAPTCHA_PRIVATE_KEY'] = os.getenv('RECAPTCHA_PRIVATE_KEY')
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from users.views import users_blueprint
from pantry.views import pantry_blueprint
from shopping.views import shopping_blueprint

app.register_blueprint(users_blueprint, url_prefix='/user')
app.register_blueprint(pantry_blueprint, url_prefix='/pantry')
app.register_blueprint(shopping_blueprint, url_prefix='/shopping')


@app.route('/')
def home():
    return render_template('base.html')


@app.route('/base')
def base():
    return render_template('base.html')


@app.route('/main-menu')
def baseLogin():
    # flash('welcome user  ' + p.username)
    return render_template('main/index.html', Foodaboutexpired=testingdata.soon_to_expire,
                           Foodexpired=testingdata.expired, expiry_date=testingdata.expiry_date,
                           used_calories=testingdata.used_calories,
                           used_items=testingdata.used_items, soon_to_expire_seven=testingdata.soon_to_expire_seven,
                           today=testingdata.today)


# username=p.username,


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
        filtered_items = [item for item in testingdata.items if
                          (min_calories is None or item['calories'] >= int(min_calories)) and
                          (max_calories is None or item['calories'] <= int(max_calories)) and
                          (not not_expired_only or (not_expired_only and datetime.datetime.strptime(item['expiry_date'],
                                                                                                    "%Y-%m-%d").date() >= testingdata.today)) and
                          (expiry_date is None or datetime.datetime.strptime(item['expiry_date'],
                                                                             "%Y-%m-%d").date() <= datetime.datetime.strptime(
                              expiry_date, "%Y-%m-%d").date())]
    return render_template('kitchen/kitchen_main.html', filtered_items=filtered_items,
                           not_yet_expire=testingdata.not_yet_expire)


if __name__ == '__main__':
    app.run(debug=True)
