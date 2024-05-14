from flask import Blueprint, render_template, request, redirect, url_for, flash

import datetime

import testingdata

kitchen_blueprint = Blueprint('pantry', __name__, template_folder='templates')

print("Template folder:", kitchen_blueprint.template_folder)

@kitchen_blueprint.route('/kitchen/recipes')
def recipe_detail():
    return render_template('kitchen/recipes.html')  # Adjust the template name as necessary


@kitchen_blueprint.route('/kitchen/kitchen_main', methods=['GET'])
def kitchen_main():
    min_calories = request.args.get('min_calories')
    max_calories = request.args.get('max_calories')
    expiry_date = request.args.get('expiry_date')
    not_expired_only = request.args.get('not_expired') == 'on'

    filtered_items = []
    if min_calories or max_calories or expiry_date or not_expired_only:
        filtered_items = [item for item in testingdata.items if
                          (min_calories is None or item['calories'] >= int(min_calories)) and
                          (max_calories is None or item['calories'] <= int(max_calories)) and
                          (not not_expired_only or (not_expired_only and datetime.datetime.strptime(item['expiry_date'],
                                                                                                    "%Y-%m-%d").date() >= today)) and
                          (expiry_date is None or datetime.datetime.strptime(item['expiry_date'],
                                                                             "%Y-%m-%d").date() <= datetime.datetime.strptime(
                              expiry_date, "%Y-%m-%d").date())]
    return render_template('kitchen/kitchen_main.html', filtered_items=filtered_items, not_yet_expire=not_yet_expire)
