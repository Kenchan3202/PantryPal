from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from models import Recipe
from app import db

import testingdata
import recipe_util

recipes_blueprint = Blueprint('recipes', __name__, template_folder='templates')

print("Template folder:", recipes_blueprint.template_folder)


# sorting recipes from highest to lowest ratings
@recipes_blueprint.route('/recipes')
@login_required
def recipe_list():
    return render_template('recipes/recipes.html')  # Adjust the template name as necessary


# add recipes function
@recipes_blueprint.route('/add_recipes')
@login_required
def add_recipe():
    return render_template('recipes/add_recipes.html')


# shows detailed view page of recipe
@recipes_blueprint.route('/view_recipe')
def view_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    return render_template('recipes/add_recipes.html', recipe=recipe) # to be updated with view recipes html

# edit recipes function
@recipes_blueprint.route('/edit_recipes')
@login_required
def edit_recipe():
    return render_template('recipes/edit_recipes.html')

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
