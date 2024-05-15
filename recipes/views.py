from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required

import testingdata

recipes_blueprint = Blueprint('recipes', __name__, template_folder='templates')

print("Template folder:", recipes_blueprint.template_folder)


@recipes_blueprint.route('/recipes')
@login_required
def recipe_list():
    return render_template('recipes/recipes.html')  # Adjust the template name as necessary


@recipes_blueprint.route('/add_recipes')
@login_required
def add_recipe():
    return render_template('recipes/add_recipes.html')


@recipes_blueprint.route('/edit_recipes')
@login_required
def edit_recipe():
    return render_template('recipes/edit_recipes.html')

@recipes_blueprint.route('/delete_recipe', methods=['POST'])
@login_required
def delete_recipe():
    return render_template('recipes/edit_recipes.html')

@recipes_blueprint.route('/rate_recipe', methods=['POST'])
@login_required
def rate_recipe():
    return render_template('recipes/edit_recipes.html')
