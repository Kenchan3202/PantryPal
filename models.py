from flask_login import UserMixin
from app import db
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

    # declaring relationships to other tables
    recipes = db.relationship('Recipe')
    shopping_lists = db.relationship('ShoppingList')

    def __init__(self, email, password, first_name, last_name, dob, role='user'):
        self.email = email
        # Hash password before storing in database
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self.first_name = first_name
        self.last_name = last_name
        self.dob = dob
        self.role = role

    def verify_password(self, password) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), self.password)


class Recipe(db.Model):
    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    method = db.Column(db.Text, nullable=False)
    serves = db.Column(db.Integer, nullable=False)
    calories = db.Column(db.Float, nullable=False)
    rating = db.Column(db.Float, nullable=True)

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
    barcodes = db.relationship('Barcode')
    shopping_items = db.relationship('ShoppingItem')

    def __init__(self, food_name):
        self.name = food_name


class Barcode(db.Model):
    __tablename__ = 'barcodes'

    id = db.Column(db.Integer, primary_key=True)
    food_item = db.Column(db.String(50), db.ForeignKey(FoodItem.name), nullable=False)  # Establish link to food table
    quantity = db.Column(db.Float)
    units = db.Column(db.String(10))

    def __init__(self, food_item, quantity, units):
        self.food_item = food_item
        self.quantity = quantity
        self.units = units


class ShoppingItem(db.Model):
    __tablename__ = 'shoppingitems'

    id = db.Column(db.Integer, primary_key=True)
    list_id = db.Column(db.Integer, db.ForeignKey(ShoppingList.id), nullable=False)
    food_item = db.Column(db.String(50), db.ForeignKey(FoodItem.name), nullable=False)

    quantity = db.Column(db.Float)
    units = db.Column(db.String(10))

    def __init__(self, list_id, food_item, quantity, units):
        self.list_id = list_id
        self.food_item = food_item
        self.quantity = quantity
        self.units = units


class PantryItem(db.Model):
    __tablename__ = 'pantryitems'
    pass


class WastedFood(db.Model):
    pass


class Ingredient(db.Model):
    pass


class Diet(db.Model):
    __tablename__ = 'diet'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(30), nullable=False, unique=True)

    compatibleDiet = db.relationship('CompatibleDiet')

    def __init__(self, description):
        self.description = description


class CompatibleDiet(db.Model):
    __tablename__ = 'compatible_diet'
    id = db.Column(db.Integer, primary_key=True)
    diet_id = db.Column(db.Integer, db.ForeignKey(Diet.id), nullable=False)

    pass
