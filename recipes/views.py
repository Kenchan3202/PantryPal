from os import abort

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

import testingdata
from recipes import recipe_util
from recipes.forms import RecipeForm
from recipes.recipe_util import create_recipe

recipes_blueprint = Blueprint('recipes', __name__, template_folder='templates')

print("Template folder:", recipes_blueprint.template_folder)
from app import db, app
from models import Recipe


@recipes_blueprint.route('/recipes')
@login_required
def recipes():
    recipes = Recipe.query.all()
    return render_template('recipes/recipes.html', recipes=recipes) #same as view recipe, but working on recipe.html


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
    return render_template('recipes/recipes_detail.html', recipe=recipe)


# @recipes_blueprint.route('/add_recipes', methods=['GET', 'POST'])
# @login_required
# def add_recipes():
#     form = RecipeForm()
#     if form.validate_on_submit():
#         ingredients = [{
#             'food': ingredient.food.data,
#             'quantity': ingredient.quantity.data,
#             'unit': ingredient.unit.data
#         } for ingredient in form.ingredients.data]
#
#         create_recipe(form.name.data, form.method.data, form.serves.data, form.calories.data, ingredients)
#
#         flash('Recipe added successfully!', 'success')
#         return redirect(url_for('recipes.recipes'))
#
#     return render_template('recipes/add_recipes.html', form=form)


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

@recipes_blueprint.route('/add_recipes')
@login_required
def add_detail():
    return render_template('recipes/add_recipes.html')


@recipes_blueprint.route('/edit_recipes')
@login_required
def edit_detail():
    return render_template('recipes/edit_recipes.html')

# sorting recipes from highest to lowest ratings
@recipes_blueprint.route('/recipes')
@login_required
def recipe_list():
    return render_template('recipes/recipes.html')  # Adjust the template name as necessary


# add recipes function
# @recipes_blueprint.route('/add_recipes')
# @login_required
# def add_recipe():
#     return render_template('recipes/add_recipes.html')


# shows detailed view page of recipe
# @recipes_blueprint.route('/view_recipe')
# def view_recipe(recipe_id):
#     recipe = Recipe.query.get_or_404(recipe_id)
#     return render_template('recipes/add_recipes.html', recipe=recipe) # to be updated with view recipes html

# edit recipes function
# @recipes_blueprint.route('/edit_recipes')
# @login_required
# def edit_recipe():
#     return render_template('recipes/edit_recipes.html')

# delete recipes function
@recipes_blueprint.route('/delete_recipe', methods=['POST'])
@login_required
def delete_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    if recipe.user_id != current_user.id: # user can only delete their own recipe
        abort(403)

    db.session.delete(recipe)
    db.session.commit()
    flash('Recipe deleted successfully!', 'success')
    return redirect(url_for('recipes.recipes'))

# rate recipes function
@recipes_blueprint.route('/rate_recipe', methods=['POST'])
@login_required
def rate_recipe():
        return render_template('recipes/edit_recipes.html')

