from flask_login import current_user

from app import db
from models import Recipe, Ingredient, QuantifiedFoodItem, FoodItem, Rating


# user_id = 1


# ingredients is a list of dictionaries in the format
# "food": "<food>"
# "quantity": <quantity>
# "unit": "<unit>"
def create_recipe(name, method, serving_size, calories, ingredients):
    new_recipe = Recipe(user_id=current_user.id,
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
    new_ingredient = Ingredient(recipe_id=recipe_id,
                                qfood_id=qfid)
    db.session.add(new_ingredient)
    db.session.commit()


def create_and_get_qfid(food_id, quantity, units):
    qfi = QuantifiedFoodItem(food_id=food_id,
                             quantity=quantity,
                             units=units)
    db.session.add(qfi)
    db.session.commit()
    qfid = qfi.id
    return qfi.id


def create_or_get_food_item(food_name):
    food = FoodItem.query.filter_by(name=food_name).first()
    if food is None:  # Add a new food_item to the database if queried food doesn't already exist
        food = FoodItem(food_name=food_name)
        db.session.add(food)
        db.session.commit()
    return food


def update_recipe_rating(recipe_id):
    # 获取所有对该食谱的评分
    ratings = Rating.query.filter_by(recipe_id=recipe_id).all()
    if ratings:
        # 计算平均评分
        total_rating = sum([rate.rating for rate in ratings])
        average_rating = total_rating / len(ratings)
        # 找到对应的食谱并更新其评分
        recipe = Recipe.query.get(recipe_id)
        if recipe:
            recipe.rating = average_rating
            db.session.commit()
            return average_rating
    return None


# Method to rate a recipe. Takes user, recipe and numeric value of rating as parameters.
# Recipe's rating value is updated as well.
def create_recipe_rating(user_id: int, recipe_id: int, rating: int) -> None:
    rating = Rating(user_id=user_id, recipe_id=recipe_id, rating=rating)
    db.session.add(rating)
    db.session.flush()
    recipe = Recipe.query.filter_by(id=recipe_id).first()
    recipe.update_rating()


# Method to delete an instance of a recipe. First all Qfooditems related to the recipe's ingredients are removed.
# All ingredients and ratings which are related to the given recipe are deleted automatically db cascading.
# Takes recipe object to be deleted as parameter.
def delete_recipe_instance(recipe: Recipe) -> None:
    qfoodids = [ingredient.qfood_id for ingredient in recipe.ingredients]
    for qfood_id in qfoodids:
        qfood = QuantifiedFoodItem.query.filter_by(id=qfood_id).first()
        db.session.delete(qfood)
    db.session.delete(recipe)
    db.session.commit()

def save_rating(user_id, recipe_id, rating):
    existing_rating = Rating.query.filter_by(user_id=user_id, recipe_id=recipe_id).first()
    if existing_rating:
        existing_rating.set_rating(rating)
    else:
        new_rating = Rating(user_id=user_id, recipe_id=recipe_id, rating=rating)
        db.session.add(new_rating)
    db.session.commit()


def get_in_use_recipes(user_id):
    # This function should return a list of recipes in use by the user
    # For demonstration purposes, let's assume we return all recipes
    return Recipe.query.filter_by(user_id=user_id).all()

# def test_create_recipe():
#     name = "improved scrambled eggs again 2"
#     method = (
#         "1. mix egg. and add cornstarch with some water 2. high heat with butter while constant stir 3. take out of "
#         "pan just before done")
#     serving_size = 2
#     calories = 120
#     ingredients = [{
#         "food": "Eggs",
#         "quantity": 4,
#         "unit": "#"
#     },
#         {
#             "food": "Butter",
#             "quantity": 20,
#             "unit": "g"
#         },
#         {
#             "food": "Corn starch",
#             "quantity": 5,
#             "unit": "g"
#         }
#     ]
#     with app.app_context():
#         create_recipe(name, method, serving_size, calories, ingredients)
#         db.session.commit()
