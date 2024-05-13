from flask_login import UserMixin
from app import db


class User(db.Model ,UserMixin):
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

    def __init__(self, email, password, ):
        pass
class Recipe:
    pass

class ShoppingItem:
    pass

class ShoppingList:
    pass

class WastedFood:
    pass

class PantryItem:
    pass

class Ingredient:
    pass

class FoodItem:
    pass

class Barcode:
    pass

class CompatibleDiet:
    pass

class Diet:
    pass