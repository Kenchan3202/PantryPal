from flask import Blueprint, render_template, request, redirect, url_for, flash

import testingdata

recipes_blueprint = Blueprint('recipes', __name__, template_folder='templates')

print("Template folder:", recipes_blueprint.template_folder)


@recipes_blueprint.route('/recipes')
def recipe_detail():
    return render_template('recipes/recipes.html')  # Adjust the template name as necessary


@recipes_blueprint.route('/add_recipes')
def recipe_detail():
    return render_template('recipes/add_recipes.html')


@recipes_blueprint.route('/edit_recipes')
def recipe_detail():
    return render_template('recipes/edit_recipes.html')
