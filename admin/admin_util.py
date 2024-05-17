from models import Recipe, ShoppingList, Rating, PantryItem, WastedFood, Ingredient, ShoppingItem, Barcode, \
    QuantifiedFoodItem, User
from app import db


def delete_user_related_data(user_id):
    # 收集与用户相关的所有数据
    recipes = Recipe.query.filter_by(user_id=user_id).all()
    ratings = Rating.query.filter_by(user_id=user_id).all()
    shopping_lists = ShoppingList.query.filter_by(user_id=user_id).all()
    pantry_items = PantryItem.query.filter_by(user_id=user_id).all()
    wasted_foods = WastedFood.query.filter_by(user_id=user_id).all()

    # 集合用于收集所有需要删除的QuantifiedFoodItem
    qfood_items_to_delete = set()

    # 删除与用户相关的食谱记录及其相关数据
    for recipe in recipes:
        ingredients = Ingredient.query.filter_by(recipe_id=recipe.id).all()
        for ingredient in ingredients:
            qfood_items_to_delete.add(ingredient.qfood_id)
            db.session.delete(ingredient)
        db.session.delete(recipe)

    # 删除与用户相关的评分记录
    for rating in ratings:
        db.session.delete(rating)

    # 删除与用户相关的购物清单记录及其相关数据
    for shopping_list in shopping_lists:
        shopping_items = ShoppingItem.query.filter_by(list_id=shopping_list.id).all()
        for shopping_item in shopping_items:
            qfood_items_to_delete.add(shopping_item.qfood_id)
            db.session.delete(shopping_item)
        db.session.delete(shopping_list)

    # 删除与用户相关的储藏室记录及其相关数据
    for pantry_item in pantry_items:
        qfood_items_to_delete.add(pantry_item.qfood_id)
        db.session.delete(pantry_item)

    # 删除与用户相关的浪费食物记录及其相关数据
    for wasted_food in wasted_foods:
        qfood_items_to_delete.add(wasted_food.qfood_id)
        db.session.delete(wasted_food)

    # 删除收集到的QuantifiedFoodItem和相关的Barcode
    for qfood_id in qfood_items_to_delete:
        barcodes = Barcode.query.filter_by(qfood_id=qfood_id).all()
        for barcode in barcodes:
            db.session.delete(barcode)
        qfood_item = QuantifiedFoodItem.query.get(qfood_id)
        if qfood_item:
            db.session.delete(qfood_item)

    # 最后删除用户记录
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)

    db.session.commit()