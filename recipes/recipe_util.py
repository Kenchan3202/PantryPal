from flask_login import current_user

from app import db, app
import models

# user_id = 1


# ingredients is a list of dictionaries in the format
# "food": "<food>"
# "quantity": <quantity>
# "unit": "<unit>"
def create_recipe(name, method, serving_size, calories, ingredients):
    new_recipe = models.Recipe(user_id=current_user.id,
                               recipe_name=name,
                               cooking_method=method,
                               serves=serving_size,
                               calories=calories)
    db.session.add(new_recipe)
    db.session.commit()
    recipe_id = new_recipe.id
    for ingredient in ingredients:
        add_ingredient(ingredient["food"], ingredient["quantity"], ingredient["unit"], new_recipe.id)


def add_ingredient(ingredient, quantity, unit, recipe_id):
    food_id = create_or_get_food_item(ingredient).id
    qfid = create_and_get_qfid(food_id, quantity, unit)
    new_ingredient = models.Ingredient(recipe_id=recipe_id,
                                       qfood_id=qfid)
    db.session.add(new_ingredient)
    db.session.commit()


def create_and_get_qfid(food_id, quantity, units):
    qfi = models.QuantifiedFoodItem(food_id=food_id,
                                    quantity=quantity,
                                    units=units)
    db.session.add(qfi)
    db.session.commit()
    qfid = qfi.id
    return qfi.id


def create_or_get_food_item(food_name):
    food = models.FoodItem.query.filter_by(name=food_name).first()
    if food is None:  # Add a new food_item to the database if queried food doesn't already exist
        food = models.FoodItem(food_name=food_name)
        db.session.add(food)
        db.session.commit()
    return food


# Method to rate a recipe. Takes user, recipe and numeric value of rating as parameters.
def rate_recipe(user_id: int, recipe_id: int, rating: int) -> None:
    rating = models.Rating(user_id=user_id, recipe_id=recipe_id, rating=rating)
    db.session.add(rating)
    db.session.flush()
    recipe = models.Recipe.query.filter_by(id=recipe_id).first()
    recipe.update_rating()


def test_create_recipe():
    name = "improved scrambled eggs again 2"
    method = (
        "1. mix egg. and add cornstarch with some water 2. high heat with butter while constant stir 3. take out of "
        "pan just before done")
    serving_size = 2
    calories = 120
    ingredients = [{
        "food": "Eggs",
        "quantity": 4,
        "unit": "#"
    },
        {
            "food": "Butter",
            "quantity": 20,
            "unit": "g"
        },
        {
            "food": "Corn starch",
            "quantity": 5,
            "unit": "g"
        }
    ]
    with app.app_context():
        create_recipe(name, method, serving_size, calories, ingredients)
        db.session.commit()
