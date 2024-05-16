# Authored by: Joe Hare & Keirav Shah
# latest edition: 14/05/2024

# File to add sample data to database instance for testing.

import random
from app import db, app
import models
pantryitems = [
    {"name": "Milk", "expiry_date": "2024-05-10", 'number': '2', 'quantity': 200, 'units': 'ml', 'calories': 200},
    {"name": "jelly", "expiry_date": "2024-05-11", 'number': '5', 'quantity': 200, 'units': 'g', 'calories': 250},
    {"name": "pork", "expiry_date": "2024-05-12", 'number': '4', 'quantity': 200,  'units': 'g', 'calories': 350},
    {"name": "chocolate", "expiry_date": "2024-05-12", 'number': '4', 'quantity': 200, 'units': 'g', 'calories': 360},
    {"name": "Goat Milk", "expiry_date": "2024-05-13", 'number': '2', 'quantity': 200, 'units': 'g', 'calories': 200},
    {"name": "Bread", "expiry_date": "2024-05-12", 'number': '2', 'quantity': 200, 'units': 'g', 'calories': 100},
    {"name": "Apple", "expiry_date": "2024-04-28", 'number': '5', 'quantity': 200, 'units': 'g', 'calories': 60},
    {"name": "Beef", "expiry_date": "2024-06-30", 'number': '5', 'quantity': 200, 'units': 'g', 'calories': 500},
    {"name": "Lamb", "expiry_date": "2024-09-28", 'number': '3', 'quantity': 200, 'units': 'g', 'calories': 450},
    {"name": "Apple juice", "expiry_date": "2024-05-04", 'number': '100', 'quantity': 200, 'units': 'ml', 'calories': 150},
]

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
userObjects = []

foodItems = ["Apple", "Tofu", "Spaghetti", "Eggs",
             "Butter", "Water", "Cornstarch",
             "Flour", "Jasmine Rice", "Basmati Rice",
             "Vegetable Oil", "Olive Oil", "Cocoa Powder",
             "Oats", "Chicken Thigh", "Chicken breast",
             "Minced Beef", "Minced Pork", "Duck breast",
             "Cinnamon", "Garlic", "Onion",
             "Shallot", "Spring Onion", "Galangal",
             "Ginger", "Rendang", "Anchovies",
             "Peanuts", "Coconut", "Salmon Fillet",
             "White Miso", "Red Miso", "Parsnip",
             "Pork Loin", "Peanut Oil", "Carrot",
             "Dashi", "Beef Chuck", "Pesto", 'Tomatoes',
             'Fresh Mozzarella', 'Fresh Basil Leaves',
             'Extra Virgin Olive Oil', 'Balsamic Vinegar',
             'Salt', 'Pepper', 'Banana', 'Peanut Butter',
             'Milk', 'Eggs', 'Butter', 'Avocado', 'Lime']
foodItemObjects = []

recipes = [
    {
        'name': 'Caprese Salad',
        'ingredients': ['Tomatoes', 'Fresh Mozzarella', 'Fresh Basil Leaves', 'Extra Virgin Olive Oil',
                        'Balsamic Vinegar', 'Salt', 'Pepper'],
        'method': 'Slice tomatoes and fresh mozzarella. Arrange them on a plate, '
                  'alternating slices. Tuck fresh basil leaves in between. Drizzle '
                  'with extra virgin olive oil and balsamic vinegar. Season with salt '
                  'and pepper to taste.'
    },
    {
        'name': 'Peanut Butter Banana Smoothie',
        'ingredients': ['Banana', 'Peanut Butter', 'Milk'],
        'method': 'Peel and slice banana. Put banana slices, peanut butter, and '
                  'milk into a blender. Add honey if desired. Blend until smooth.'
    },
    {
        'name': 'Scrambled Eggs',
        'ingredients': ['Eggs', 'Butter', 'Salt', 'Pepper'],
        'method': 'Crack eggs into a bowl and beat them until yolks and whites are combined. '
                  'Melt butter in a non-stick skillet over medium heat. Pour in beaten eggs. '
                  'Stir occasionally until eggs are set. Season with salt and pepper.'
    },
    {
        'name': 'Guacamole',
        'ingredients': ['Avocado', 'Lime', 'Salt'],
        'method': 'Cut avocado in half, remove pit, and scoop out flesh into a bowl. '
                  'Mash avocado with a fork. Squeeze lime juice over mashed avocado '
                  'and mix well. Add salt to taste.'
    }
]
recipeObjects = []


def add_sample_users():
    for user in users:
        new_user = models.User(email=user['email'],
                               password=user['password'],
                               first_name=user['first_name'],
                               last_name=user['last_name'],
                               dob=user['dob'])
        userObjects.append(new_user)
        db.session.add(new_user)
    db.session.commit()


def add_food_items():
    for food in foodItems:
        new_food = models.FoodItem(food_name=food)
        foodItemObjects.append(new_food)
        db.session.add(new_food)
    db.session.commit()


def create_quantified_food_item(food_item_id: int, quantity=0) -> models.QuantifiedFoodItem:
    units = ('ml', 'g')
    quantities = (200, 500, 1000, 750, 50, 20)
    quant = quantity if quantity else random.choice(quantities)
    q_fooditem = models.QuantifiedFoodItem(food_id=food_item_id,
                                           quantity=quant,
                                           units=random.choice(units))
    db.session.add(q_fooditem)
    db.session.commit()
    return q_fooditem


def create_pantry_item(user_id: int) -> models.PantryItem:
    expiries = ('05/08/2024', '10/11/2024', '18/08/2024', '02/04/2024', '01/01/2025', '28/03/2025', '19/09/2024')
    qfood_item = create_quantified_food_item(random.choice(foodItemObjects).id)
    pantry_item = models.PantryItem(user_id=user_id, qfood_id=qfood_item.id, expiry=random.choice(expiries))
    db.session.add(pantry_item)
    db.session.commit()
    return pantry_item


def create_pantries() -> None:
    for user in userObjects:
        num_items = random.choice((0, 3, 8, 6, 4, 8))
        for i in range(num_items):
            create_pantry_item(user_id=user.id)


def create_ingredient(recipe_id: int, qfood_id: int) -> models.Ingredient:
    # recipe = models.Recipe.query.filter_by(name=recipe_name).first()
    ingredient = models.Ingredient(recipe_id=recipe_id, qfood_id=qfood_id)
    db.session.add(ingredient)
    db.session.commit()
    return ingredient


def create_recipe_object(user_id: int, recipe) -> models.Recipe:
    new_recipe = models.Recipe(user_id=user_id,
                               recipe_name=recipe['name'],
                               cooking_method=recipe['method'],
                               serves=random.choice((1, 2, 4)),
                               calories=random.choice((450, 800, 1200, 1000)))

    db.session.add(new_recipe)
    db.session.flush()
    db.session.refresh(new_recipe)
    recipeObjects.append(new_recipe)

    for ingredient in recipe['ingredients']:
        foodItem = models.FoodItem.query.filter_by(name=ingredient).first()
        qfoodItem = create_quantified_food_item(foodItem.id)
        create_ingredient(recipe_id=new_recipe.id, qfood_id=qfoodItem.id)
    db.session.commit()
    return new_recipe


def create_recipes() -> None:
    for recipe in recipes:
        user_id = random.choice(userObjects).id
        create_recipe_object(user_id=user_id, recipe=recipe)


def create_shopping_items(list_id: int, user_id: int) -> models.ShoppingItem:
    # s_list = models.ShoppingList.query.filter_by(user_id=user_id).first()
    qfood_item = create_quantified_food_item(random.choice(foodItemObjects).id)
    shopping_item = models.ShoppingItem(list_id=list_id, qfood_id=qfood_item.id)
    db.session.add(shopping_item)
    db.session.commit()
    return shopping_item


def create_shopping_lists() -> None:
    chosen_users = userObjects[::2]
    for user in chosen_users:
        for x in range(2):
            shopping_list = models.ShoppingList(user.id)
            db.session.add(shopping_list)
            db.session.flush()
            db.session.refresh(shopping_list)
            num_items = random.choice((3, 5, 2, 6, 9))
            for i in range(num_items):
                create_shopping_items(list_id=shopping_list.id, user_id=user.id)


def main():
    # add sample users
    add_sample_users()

    # add sample foodItems
    add_food_items()

    # create pantries
    create_pantries()

    # create recipes
    create_recipes()

    # create shopping lists
    create_shopping_lists()


if __name__ == '__main__':
    with app.app_context():
        models.init_db()
        main()
        db.session.commit()
