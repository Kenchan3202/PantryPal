# Authored by: Joe Hare & Keirav Shah
# latest edition: 14/05/2024

# File to add sample data to database instance for testing.

import models
from app import db, app

users = [
    {"first_name": "Gillan", "last_name": "Athelstan", "email": "gathelstan0@npr.org", "password": "pO6>#*9hV",
     "dob": "6/2/2023"},
    {"first_name": "Doralyn", "last_name": "Kosel", "email": "dkosel1@noaa.gov", "password": "aX7|S&9hZrRT",
     "dob": "11/27/2023"},
    {"first_name": "Patrice", "last_name": "Ferier", "email": "pferier2@google.it", "password": "bX3%UvGx$nl@g",
     "dob": "7/18/2023"},
    {"first_name": "Dyann", "last_name": "Shaul", "email": "dshaul3@mashable.com", "password": "cO5{hmv_UiO>LDa.",
     "dob": "11/30/2023"},
    {"first_name": "Graeme", "last_name": "Aliman", "email": "galiman4@discuz.net", "password": "vX5$0rJyY20=|",
     "dob": "6/14/2023"},
    {"first_name": "Rutledge", "last_name": "Dicey", "email": "rdicey5@ning.com", "password": "vG6\\XecCNVG`#di(",
     "dob": "3/11/2024"},
    {"first_name": "Arleyne", "last_name": "Ianetti", "email": "aianetti6@xinhuanet.com", "password": "kQ0.B4!@wuUp#7u",
     "dob": "4/9/2024"},
    {"first_name": "Jemmy", "last_name": "Sambals", "email": "jsambals7@narod.ru", "password": "lY2*_{*\\F'CZ7Y",
     "dob": "8/6/2023"},
    {"first_name": "Leila", "last_name": "Jirek", "email": "ljirek8@addthis.com", "password": "yR6~).,!2+`R",
     "dob": "11/29/2023"},
    {"first_name": "Chrysler", "last_name": "Quemby", "email": "cquemby9@dion.ne.jp", "password": "eB3_Xk\\f",
     "dob": "4/2/2024"}
]

foodItems = ["tomato", "apple", "banana",
             "tofu", "spaghetti", "eggs",
             "butter", "water", "cornstarch",
             "plain flour", "jasmine rice", "basmati rice",
             "vegetable oil", "olive oil", "cocoa powder",
             "oats", "chicken thigh", "chicken breast",
             "minced beef", "minced pork", "duck breast",
             "cinnamon", "garlic", "onion",
             "shallot", "spring onion", "galangal",
             "ginger", "rendang", "anchovies",
             "peanuts", "coconut", "salmon fillet",
             "white miso", "red miso", "parsnip",
             "pork loin", "peanut oil", "carrot",
             "dashi", "beef chuck", "pesto"]


def add_food_items():
    with app.app_context():
        for food in foodItems:
            new_food = models.FoodItem(food_name=food)
            db.session.add(new_food)
        db.session.commit()


def add_sample_users():
    with app.app_context():
        for user in users:
            new_user = models.User(email=user['email'],
                                   password=user['password'],
                                   first_name=user['first_name'],
                                   last_name=user['last_name'],
                                   dob=user['dob'])
            db.session.add(new_user)
        db.session.commit()
