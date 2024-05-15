# Authored by: Joe Hare & Keirav Shah
# latest edition: 14/05/2024

from flask_login import UserMixin
from app import db, app
from datetime import datetime
import bcrypt


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    # authentication details
    email = db.Column(db.String(75), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)

    # user details
    first_name = db.Column(db.String(50), nullable=False, unique=False)
    last_name = db.Column(db.String(50), nullable=False, unique=False)
    dob = db.Column(db.String(10), nullable=False)
    role = db.Column(db.String(100), nullable=False, default='user')
    registered_on = db.Column(db.DateTime, nullable=False)

    # declaring relationships to other tables
    recipes = db.relationship('Recipe')
    shopping_lists = db.relationship('ShoppingList')
    pantry = db.relationship("PantryItem")
    wasted = db.relationship('WastedFood')

    def __init__(self, email, password, first_name, last_name, dob, role='user'):
        self.email = email
        # Hash password before storing in database
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self.first_name = first_name
        self.last_name = last_name
        self.dob = dob
        self.registered_on = datetime.now()
        self.role = role

    def verify_password(self, password) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), self.password)

    def set_password(self, password):
        """Create hashed password."""
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

class Recipe(db.Model):
    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    method = db.Column(db.Text, nullable=False)
    serves = db.Column(db.Integer, nullable=False)
    calories = db.Column(db.Float, nullable=True)
    rating = db.Column(db.Float, nullable=True)

    # Links to other tables
    ingredients = db.relationship("Ingredient")
    compatible_diets = db.relationship("CompatibleDiet")

    def __init__(self, user_id, recipe_name, cooking_method, serves, calories):
        self.user_id = user_id
        self.name = recipe_name
        self.method = cooking_method
        self.serves = serves
        self.calories = calories
        self.rating = 0


class ShoppingList(db.Model):
    __tablename__ = 'shoppinglists'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)

    # Declaring relationship shopping item table
    shopping_items = db.relationship('ShoppingItem')

    def __init__(self, user_id):
        self.user_id = user_id


class FoodItem(db.Model):
    __tablename__ = 'fooditems'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    # Declaring relationships to other tables
    quantified_food_item = db.relationship('QuantifiedFoodItem')

    def __init__(self, food_name):
        self.name = food_name


class QuantifiedFoodItem(db.Model):
    __tablename__ = 'quantifiedfooditem'

    id = db.Column(db.Integer, primary_key=True)
    food_id = db.Column(db.Integer, db.ForeignKey(FoodItem.id), nullable=False)
    quantity = db.Column(db.Float, default=0.0)
    units = db.Column(db.String(5), default="g")

    # References to other tables
    shopping = db.relationship('ShoppingItem')
    ingredients = db.relationship('Ingredient')
    pantries = db.relationship('PantryItem')
    wasted = db.relationship('WastedFood')
    barcodes = db.relationship('Barcode')

    def __init__(self, food_id, quantity, units):
        self.food_id = food_id
        self.quantity = quantity
        self.units = units


class ShoppingItem(db.Model):
    __tablename__ = 'shoppingitems'

    id = db.Column(db.Integer, primary_key=True)
    list_id = db.Column(db.Integer, db.ForeignKey(ShoppingList.id), nullable=False)
    qfood_id = db.Column(db.String(50), db.ForeignKey(QuantifiedFoodItem.id), nullable=False)

    def __init__(self, list_id, qfood_id):
        self.list_id = list_id
        self.qfood_id = qfood_id


class Ingredient(db.Model):
    __tablename__ = 'ingredients'

    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey(Recipe.id), nullable=False)
    qfood_id = db.Column(db.Integer, db.ForeignKey(QuantifiedFoodItem.id), nullable=False)

    def __init__(self, recipe_id, qfood_id):
        self.recipe_id = recipe_id
        self.qfood_id = qfood_id


class PantryItem(db.Model):
    __tablename__ = 'pantryitems'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    qfood_id = db.Column(db.Integer, db.ForeignKey(QuantifiedFoodItem.id), nullable=False)
    expiry = db.Column(db.String(10), nullable=True)

    def __init__(self, user_id, qfood_id, expiry):
        self.user_id = user_id
        self.qfood_id = qfood_id
        self.expiry = expiry


class WastedFood(db.Model):
    __tablename__ = 'wastedfood'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    qfood_id = db.Column(db.Integer, db.ForeignKey(QuantifiedFoodItem.id), nullable=False)
    expired = db.Column(db.String(10), nullable=True)

    def __init__(self, user_id, qfood_id, expired):
        self.user_id = user_id
        self.qfood_id = qfood_id
        self.expired = expired


class Barcode(db.Model):
    __tablename__ = 'barcodes'

    id = db.Column(db.Integer, primary_key=True)
    qfood_id = db.Column(db.Integer, db.ForeignKey(QuantifiedFoodItem.id), nullable=False)  # Establish link to food table
    barcode = db.Column(db.String(15), nullable=False)

    def __init__(self, qfood_id, barcode):
        self.qfood_id = qfood_id
        self.barcode = barcode


class Diet(db.Model):
    __tablename__ = 'diet'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(30), nullable=False, unique=True)

    # link to other tables
    compatibleDiet = db.relationship('CompatibleDiet')

    def __init__(self, description):
        self.description = description


class CompatibleDiet(db.Model):
    __tablename__ = 'compatiblediet'
    id = db.Column(db.Integer, primary_key=True)
    diet_id = db.Column(db.Integer, db.ForeignKey(Diet.id), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey(Recipe.id), nullable=False)

    def __init__(self, diet_id, recipe_id):
        self.diet_id = diet_id
        self.recipe_id = recipe_id


def init_db():
    # with app.app_context():
    db.drop_all()
    db.create_all()
    admin = User(email='admin@email.com',
                 password='Admin1!',
                 first_name='Alice',
                 last_name='Jones',
                 dob='12/09/2001',
                 role='admin')
    db.session.add(admin)
    db.session.commit()
