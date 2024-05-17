from os import abort
from app import db, app
from crawler import fetch_wikipedia_description
from models import Recipe, Ingredient, QuantifiedFoodItem, Rating, PantryItem, InUseRecipe, FoodItem
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from sqlalchemy import func

from recipes.forms import RecipeForm
from recipes.recipe_util import (create_recipe, create_or_get_food_item, create_and_get_qfid, create_recipe_rating,
                                 delete_recipe_instance, get_in_use_recipes)

recipes_blueprint = Blueprint('recipes', __name__, template_folder='templates')

print("Template folder:", recipes_blueprint.template_folder)


# filter system to sort recipes based on name, calories, rating, etc.
@recipes_blueprint.route('/recipes', methods=['GET'])
@login_required
def recipes():
    can_make_recipe_filter = request.args.get('can_make', type=bool)
    sort_by = request.args.get('sort_by', 'name')
    min_calories = request.args.get('min_calories', type=int)
    max_calories = request.args.get('max_calories', type=int)
    min_rating = request.args.get('min_rating', type=int)
    ingredient_filter = request.args.get('ingredient')
    serves_filter = request.args.get('serves', type=int)

    user_pantry = PantryItem.query.filter_by(user_id=current_user.id).all()
    user_food_id_list = [item.qfood_id for item in user_pantry]

    query = Recipe.query

    # 筛选卡路里范围
    if min_calories is not None:
        query = query.filter(Recipe.calories >= min_calories)
    if max_calories is not None:
        query = query.filter(Recipe.calories <= max_calories)

    # 筛选评分
    if min_rating is not None:
        query = query.filter(Recipe.rating >= min_rating)

    # 筛选食材
    if ingredient_filter:
        query = query.join(Recipe.ingredients).join(Ingredient.qfooditem).join(FoodItem).filter(
            FoodItem.name.ilike(f"%{ingredient_filter}%"))

    # 筛选人数
    if serves_filter:
        query = query.filter(Recipe.serves == serves_filter)

    # 排序
    if sort_by == 'calories':
        query = query.order_by(Recipe.calories)
    elif sort_by == 'rating':
        query = query.order_by(Recipe.rating.desc())

    # 执行查询
    recipes = query.all()

    # 检查哪些食谱用户可以做
    if can_make_recipe_filter:
        filtered_recipes = []
        for recipe in recipes:
            can_make_recipe = True
            for ingredient in recipe.ingredients:
                pantry_item = next((item for item in user_pantry if item.qfood_id == ingredient.qfood_id), None)
                if not pantry_item or pantry_item.qfooditem.quantity < ingredient.qfooditem.quantity:
                    can_make_recipe = False
                    break
            if can_make_recipe:
                filtered_recipes.append(recipe)
        recipes = filtered_recipes

    return render_template('recipes/recipes.html', recipes=recipes)



# view own recipe
@recipes_blueprint.route('/your_recipes')
@login_required
def your_recipes():
    user_id = current_user.id
    recipes = Recipe.query.filter_by(user_id=user_id).all()
    return render_template('recipes/your_recipes.html', recipes=recipes)


# view descriptions of recipe
@recipes_blueprint.route('/recipes_detail/<int:recipe_id>')
@login_required
def recipes_detail(recipe_id):
    recipe = Recipe.query.get(recipe_id)
    ingredients = Ingredient.query.filter_by(recipe_id=recipe_id).all()

    user_food_id_list = []
    user_pantry = PantryItem.query.filter_by(user_id=current_user.id).all()
    for user_ingredient in user_pantry:
        qfi = QuantifiedFoodItem.query.filter_by(id=user_ingredient.qfood_id).first()
        user_food_id_list.append(qfi.food_id)

    recipes_with_stock_check = []

    ingredient_food_id_list = []
    for ingredient in recipe.ingredients:
        qfi = QuantifiedFoodItem.query.filter_by(id=ingredient.qfood_id).first()
        ingredient_food_id_list.append(qfi.food_id)
    can_make_recipe = True
    for id in ingredient_food_id_list:
        if id not in user_food_id_list:
            can_make_recipe = False
    recipes_with_stock_check.append({"Recipe": recipe,
                                     "Can be made": can_make_recipe})
    return render_template('recipes/recipes_detail.html', recipe=recipe, ingredients=ingredients,
                               recipes_with_stock_check=recipes_with_stock_check)


# add recipe
@recipes_blueprint.route('/add_recipes', methods=['GET', 'POST'])
@login_required
def add_recipes():
    if request.method == 'POST':
        # 获取表单数据
        name = request.form['name']
        method = request.form['method']
        serves = request.form['serves']
        calories = request.form['calories']
        ingredients = []

        for i in range(len(request.form.getlist('ingredient[]'))):
            ingredients.append({
                "food": request.form.getlist('ingredient[]')[i],
                "quantity": request.form.getlist('quantity[]')[i],
                "unit": request.form.getlist('unit[]')[i],
            })

        create_recipe(name, method, serves, calories, ingredients)
        return redirect(url_for('recipes.recipes'))  # 确保这个重定向到正确的视图
    else:
        return render_template('recipes/add_recipes.html')


# edit own recipe
@recipes_blueprint.route('/edit_recipes/<int:recipe_id>', methods=['GET', 'POST'])
@login_required
def edit_recipes(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    if request.method == 'POST':
        recipe.name = request.form['name']
        recipe.method = request.form['method']
        recipe.serves = request.form['serves']
        recipe.calories = request.form['calories']

        # 清除现有的配料
        Ingredient.query.filter_by(recipe_id=recipe_id).delete()

        # 添加新的配料
        ingredients = zip(request.form.getlist('ingredient[]'),
                          request.form.getlist('quantity[]'),
                          request.form.getlist('unit[]'))
        for food, quantity, unit in ingredients:
            food_item = create_or_get_food_item(food)
            qfi = create_and_get_qfid(food_item.id, quantity, unit)
            new_ingredient = Ingredient(recipe_id=recipe_id, qfood_id=qfi)
            db.session.add(new_ingredient)

        db.session.commit()
        flash('Recipe updated successfully!', 'success')
        return redirect(url_for('recipes.recipes'))
    else:
        ingredients = [(i.qfooditem.fooditem.name, i.qfooditem.quantity, i.qfooditem.units) for i in recipe.ingredients]
        return render_template('recipes/edit_recipes.html', recipe=recipe, ingredients=ingredients)


# delete own recipe
@recipes_blueprint.route('/delete_recipe/<int:recipe_id>')
@login_required
def delete_recipe(recipe_id):
    recipe_to_delete = Recipe.query.filter_by(id=recipe_id).first()
    delete_recipe_instance(recipe_to_delete)
    flash('Recipe deleted successfully!', 'success')
    return redirect(url_for('recipes.recipes'))


# rate own recipe
@recipes_blueprint.route('/rate_recipe/<int:recipe_id>', methods=['POST'])
@login_required
def rate_recipe(recipe_id):
    rating_value = request.form.get('rating')
    if not rating_value:
        flash('Please select a rating.', 'error')
        return redirect(url_for('recipes.recipes', recipe_id=recipe_id))

    # Find existing rating or create a new one
    rating = Rating.query.filter_by(user_id=current_user.id, recipe_id=recipe_id).first()
    if rating:
        rating.set_rating(int(rating_value))
        flash('Your rating has been updated!', 'info')
    else:
        create_recipe_rating(user_id=current_user.id, recipe_id=recipe_id, rating=int(rating_value))
        flash('Thank you for rating!', 'success')
    return redirect(url_for('recipes.recipes', recipe_id=recipe_id))

# @app.route('/use_recipe', methods=['POST'])
# def use_recipe():
#     data = request.json
#     user_id = data.get('user_id')
#     recipe_id = data.get('recipe_id')
#
#     recipe = Recipe.query.get(recipe_id)
#     if not recipe or not recipe.ingredients:
#         return jsonify({"message": "Recipe not found or has no ingredients."}), 400
#
#     in_use_recipe = InUseRecipe(user_id=user_id, recipe_id=recipe_id)
#     db.session.add(in_use_recipe)
#     db.session.commit()
#
#     return jsonify({"message": "Recipe marked as in use."}), 200
#
#
#
# @app.route('/complete_recipe', methods=['POST'])
# def complete_recipe():
#     data = request.json
#     user_id = data.get('user_id')
#     recipe_id = data.get('recipe_id')
#
#     in_use_recipe = InUseRecipe.query.filter_by(user_id=user_id, recipe_id=recipe_id).first()
#
#     if in_use_recipe:
#         # Remove ingredients from pantry
#         recipe = in_use_recipe.recipe
#         for ingredient in recipe.ingredients:
#             pantry_item = PantryItem.query.filter_by(user_id=user_id, qfood_id=ingredient.qfood_id).first()
#             if pantry_item:
#                 pantry_item.set_quantity(pantry_item.get_quantity() - ingredient.get_quantity())
#                 if pantry_item.get_quantity() <= 0:
#                     db.session.delete(pantry_item)
#
#         db.session.delete(in_use_recipe)
#         db.session.commit()
#         return jsonify({"message": "Recipe completed and ingredients used."}), 200
#     else:
#         return jsonify({"message": "In-use recipe not found."}), 404
#
#
#
#
#
#
# @recipes_blueprint.route('/in_use_recipes', methods=['GET'])
# @login_required
# def in_use_recipes():
#     in_use_recipes = get_in_use_recipes(current_user.id)
#     return render_template('recipes/in_use_recipes.html', in_use_recipes=in_use_recipes)


