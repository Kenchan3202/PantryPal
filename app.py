import datetime
import os
from logging.handlers import RotatingFileHandler
import logging
from flask import Flask, render_template, request, redirect, url_for, session, flash
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, logout_user, login_required, current_user, LoginManager

load_dotenv()

app = Flask(__name__)
app.secret_key = 'your_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = 'users.login'

log_path = 'app.log'

handler = RotatingFileHandler(log_path, maxBytes=500000, backupCount=10)
handler.setLevel(logging.INFO)
formatter = logging.Formatter(
    "[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")
handler.setFormatter(formatter)
app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['ENCRYPTION_KEY'] = os.getenv('ENCRYPTION_KEY')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['RECAPTCHA_PUBLIC_KEY'] = os.getenv('RECAPTCHA_PUBLIC_KEY')
app.config['RECAPTCHA_PRIVATE_KEY'] = os.getenv('RECAPTCHA_PRIVATE_KEY')
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# initialise database
db = SQLAlchemy()
db.init_app(app)

from users.views import users_blueprint
from pantry.views import pantry_blueprint
from shopping.views import shopping_blueprint
from kitchen.views import kitchen_blueprint
from recipes.views import recipes_blueprint
from admin.views import admin_blueprint

app.register_blueprint(users_blueprint, url_prefix='/user')
app.register_blueprint(pantry_blueprint, url_prefix='/pantry')
app.register_blueprint(shopping_blueprint, url_prefix='/shopping')
app.register_blueprint(kitchen_blueprint, url_prefix='/kitchen')
app.register_blueprint(recipes_blueprint, url_prefix='/recipes')
app.register_blueprint(admin_blueprint, url_prefix='/admin')



@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))


@app.route('/')
def home():
    return render_template('base.html')


@app.route('/base')
def base():
    return render_template('base.html')


@app.route('/main-menu')
@login_required
def baseLogin():
    from models import PantryItem

    user_id = current_user.id

    today = datetime.date.today()
    seven_days_later = today + datetime.timedelta(days=7)

    # 获取所有当前用户的 PantryItem
    pantry_items = PantryItem.query.filter_by(user_id=user_id).all()

    soon_to_expire_seven = []
    used_items = []

    for item in pantry_items:
        try:
            expiry_date = datetime.datetime.strptime(item.get_expiry(), "%Y-%m-%d").date()
        except ValueError:
            continue  # 处理错误日期格式

        if today <= expiry_date <= seven_days_later:
            soon_to_expire_seven.append(item)
        if expiry_date <= today:
            used_items.append(item)

    return render_template('main/index.html', soon_to_expire_seven=soon_to_expire_seven, used_items=used_items,
                           today=today)


if __name__ == '__main__':
    app.run(debug=True)
