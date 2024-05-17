from os import abort

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from sqlalchemy import func

import testingdata
from recipes import recipe_util
from recipes.forms import RecipeForm
from recipes.recipe_util import create_recipe, create_or_get_food_item, create_and_get_qfid

recipes_blueprint = Blueprint('recipes', __name__, template_folder='templates')

print("Template folder:", recipes_blueprint.template_folder)
from app import db, app
from models import Recipe, Ingredient, QuantifiedFoodItem, Rating


# filter system to sort recipes based on name, calories, rating, etc.
@recipes_blueprint.route('/recipes', methods=['GET'])
@login_required
def recipes():
    # 获取排序和筛选参数
    sort_by = request.args.get('sort_by', 'name')  # 默认按名称排序
    min_calories = request.args.get('min_calories', type=int)
    max_calories = request.args.get('max_calories', type=int)
    min_rating = request.args.get('min_rating', type=int)
    ingredient_filter = request.args.get('ingredient')
    serves_filter = request.args.get('serves', type=int)

    # 开始构建查询
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
        query = query.join(Recipe.ingredients).join(Ingredient.qfooditem).filter(
            Ingredient.qfooditem.has(food_name=ingredient_filter))

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
    return render_template('recipes/recipes_detail.html', recipe=recipe, ingredients=ingredients)

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
    recipe = Recipe.query.get_or_404(recipe_id)  # 从数据库获取特定食谱
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
    ingredients = Ingredient.query.filter_by(recipe_id=recipe_id).all()
    ratings = Rating.query.filter_by(recipe_id=recipe_id).all()
    for ingredients in ingredients:
        qfood_item = QuantifiedFoodItem.query.get(ingredients.qfood_id)
        if qfood_item:
            db.session.delete(qfood_item)
        db.session.delete(ingredients)

    for ratings in ratings:
        db.session.delete(ratings)
    recipe = Recipe.query.get_or_404(recipe_id)
    db.session.delete(recipe)
    db.session.commit()
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
        rating.rating = int(rating_value)
        flash('Your rating has been updated!', 'info')
    else:
        rating = Rating(user_id=current_user.id, recipe_id=recipe_id, rating=int(rating_value))
        db.session.add(rating)
        flash('Thank you for rating!', 'success')

    db.session.commit()

    # Calculate the new average rating
    new_avg_rating = db.session.query(func.avg(Rating.rating)).filter(Rating.recipe_id == recipe_id).scalar()
    new_avg_rating = round(new_avg_rating, 1) if new_avg_rating else 0

    # Update the recipe's rating
    recipe = Recipe.query.get(recipe_id)
    recipe.rating = new_avg_rating
    db.session.commit()

    return redirect(url_for('recipes.recipes', recipe_id=recipe_id))



