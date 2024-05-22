from flask_login import current_user

from app import db
from models import Recipe, Ingredient, QuantifiedFoodItem, FoodItem, Rating, create_and_get_qfid, \
    create_or_get_food_item, PantryItem, ShoppingList, ShoppingItem


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


def create_shopping_list_from_recipe(recipe_id, user_id):
    recipe = Recipe.query.get(recipe_id)
    if not recipe:
        return {'error': 'Recipe not found'}

    user_pantry = PantryItem.query.filter_by(user_id=user_id).all()
    pantry_dict = {item.qfooditem.fooditem.name: item for item in user_pantry}

    shopping_list = ShoppingList.query.filter_by(user_id=user_id, list_name=recipe.name).first()
    if not shopping_list:
        shopping_list = ShoppingList(user_id=user_id, list_name=recipe.name)
        db.session.add(shopping_list)
        db.session.commit()

    for ingredient in recipe.ingredients:
        qfi_ingredient = QuantifiedFoodItem.query.get(ingredient.qfood_id)
        if qfi_ingredient:
            ingredient_name = qfi_ingredient.fooditem.name
            ingredient_quantity = qfi_ingredient.quantity

            pantry_item = pantry_dict.get(ingredient_name)
            if not pantry_item or pantry_item.qfooditem.quantity < ingredient_quantity:
                missing_quantity = ingredient_quantity - pantry_dict.get(ingredient_name, 0)
                newQFI = QuantifiedFoodItem(food_id=qfi_ingredient.food_id, quantity=missing_quantity, units=qfi_ingredient.units)
                db.session.add(newQFI)
                db.session.commit()

                new_shopping_item = ShoppingItem(list_id=shopping_list.id, qfood_id=newQFI.id)
                db.session.add(new_shopping_item)
                db.session.commit()

    return {'success': 'Shopping list created'}