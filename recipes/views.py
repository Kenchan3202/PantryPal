from os import abort

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

import testingdata
from recipes import recipe_util
from recipes.forms import RecipeForm
from recipes.recipe_util import create_recipe, create_or_get_food_item, create_and_get_qfid

recipes_blueprint = Blueprint('recipes', __name__, template_folder='templates')

print("Template folder:", recipes_blueprint.template_folder)
from app import db, app
from models import Recipe, Ingredient, QuantifiedFoodItem


@recipes_blueprint.route('/recipes')
@login_required
def recipes():
    recipes = Recipe.query.all()
    return render_template('recipes/recipes.html', recipes=recipes)  # same as view recipe, but working on recipe.html


@recipes_blueprint.route('/your_recipes')
@login_required
def your_recipes():
    user_id = current_user.id
    recipes = Recipe.query.filter_by(user_id=user_id).all()
    return render_template('recipes/your_recipes.html', recipes=recipes)


@recipes_blueprint.route('/recipes_detail/<int:recipe_id>')
@login_required
def recipes_detail(recipe_id):
    recipe = Recipe.query.get(recipe_id)
    ingredients = Ingredient.query.filter_by(recipe_id=recipe_id).all()
    return render_template('recipes/recipes_detail.html', recipe=recipe, ingredients=ingredients)


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


# delete recipes function
@recipes_blueprint.route('/delete_recipe/<int:recipe_id>')
@login_required
def delete_recipe(recipe_id):
    ingredients = Ingredient.query.filter_by(recipe_id=recipe_id).all()
    for ingredients in ingredients:
        qfood_item = QuantifiedFoodItem.query.get(ingredients.qfood_id)
        if qfood_item:
            db.session.delete(qfood_item)
        db.session.delete(ingredients)
    recipe = Recipe.query.get_or_404(recipe_id)
    db.session.delete(recipe)
    db.session.commit()
    flash('Recipe deleted successfully!', 'success')
    return redirect(url_for('recipes.recipes'))


# rate recipes function
@recipes_blueprint.route('/rate_recipe', methods=['POST'])
@login_required
def rate_recipe():
    return render_template('recipes/edit_recipes.html')
