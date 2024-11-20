from models.ingredient import Ingredient
from models.icecreamshop import IceCreamShop
from database.db import db
from flask import Blueprint, jsonify, render_template, request, redirect, url_for

ingredient_blueprint = Blueprint("ingredient_bp", __name__)


@ingredient_blueprint.route("/ingredients")
def index():
    ingredients = Ingredient.query.all()
    return render_template("all_ingredients.html", ingredients=ingredients)


@ingredient_blueprint.route("/<id>/ingredients")
def ingredients(id):
    icecreamshop = IceCreamShop.query.filter_by(id=id).first()
    if icecreamshop is None:
        return jsonify({
            "error": "IceCreamShop not found",
            "message": f"No ice cream shop found with id: {id}"
        }), 404
    return render_template(
        "ingredients.html", 
        ingredients=icecreamshop.ingredients,
        icecreamshop=icecreamshop
    )


@ingredient_blueprint.route("/<id>/stock/<id_ingredient>")
def stock(id, id_ingredient):
    icecreamshop = IceCreamShop.query.filter_by(id=id).first()
    if icecreamshop is None:
        return jsonify({
            "error": "IceCreamShop not found",
            "message": f"No ice cream shop found with id: {id}"
        }), 404

    ingredient = Ingredient.query.get(id_ingredient)
    if ingredient is None:
        return jsonify({
            "error": "Ingredient not found",
            "message": f"No ingredient found with id: {id_ingredient}"
        }), 404

    old_stock = ingredient.stock
    ingredient.stock_up()
    db.session.commit()
    return jsonify({
        "success": True,
        "message": f"Stocked up {ingredient.name}",
        "new_stock": ingredient.stock,
        "old_stock": old_stock
    }), 200


@ingredient_blueprint.route("/<id>/renew/<id_ingredient>")
def renew(id, id_ingredient):
    icecreamshop = IceCreamShop.query.filter_by(id=id).first()
    if icecreamshop is None:
        return jsonify({
            "error": "IceCreamShop not found",
            "message": f"No ice cream shop found with id: {id}"
        }), 404

    ingredient = Ingredient.query.get(id_ingredient)
    if ingredient is None:
        return jsonify({
            "error": "Ingredient not found",
            "message": f"No ingredient found with id: {id_ingredient}"
        }), 404

    try:
        ingredient.renew_stock()
        db.session.commit()
        return jsonify({
            "success": True,
            "message": f"Renewed {ingredient.name}",
            "new_stock": ingredient.stock
        })
    except ValueError as e:
        return jsonify({
            "success": False,
            "error": "Base ingredients cannot be renewed",
            "message": str(e)
        }), 400


@ingredient_blueprint.route("/ingredients/<id_ingredient>/is_healthy")
def is_healthy(id_ingredient):
    ingredient = Ingredient.query.get(id_ingredient)
    if ingredient is None:
        return jsonify({
            "error": "Ingredient not found",
            "message": f"No ingredient found with id: {id_ingredient}"
        }), 404
    return f"Is healthy: {ingredient.its_healthy()}"


@ingredient_blueprint.route("/ingredients/<id_ingredient>/stock_up")
def stock_up(id_ingredient):
    ingredient = Ingredient.query.get(id_ingredient)
    if ingredient is None:
        return jsonify({
            "error": "Ingredient not found",
            "message": f"No ingredient found with id: {id_ingredient}"
        }), 404
    ingredient.stock_up()
    db.session.commit()
    return f"Stock up: {ingredient.name}"


@ingredient_blueprint.route("/ingredients/<id_ingredient>/renew_stock")
def renew_stock(id_ingredient):
    ingredient = Ingredient.query.get(id_ingredient)
    if ingredient is None:
        return jsonify({
            "error": "Ingredient not found",
            "message": f"No ingredient found with id: {id_ingredient}"
        }), 404
    try:
        ingredient.renew_stock()
    except ValueError as e:
        return jsonify({
            "error": "Base ingredients cannot be renewed",
            "message": str(e)
        }), 400
    db.session.commit()
    return f"Renewed ingredient: {ingredient.name}"


@ingredient_blueprint.route("/<id>/ingredients/new")
def new(id):
    icecreamshop = IceCreamShop.query.filter_by(id=id).first()
    if icecreamshop is None:
        return jsonify({
            "error": "IceCreamShop not found",
            "message": f"No ice cream shop found with id: {id}"
        }), 404
    return render_template("new_ingredient.html", icecreamshop=icecreamshop)


@ingredient_blueprint.route("/<id>/ingredients/create", methods=["POST"])
def create(id):
    icecreamshop = IceCreamShop.query.filter_by(id=id).first()
    if icecreamshop is None:
        return jsonify({
            "error": "IceCreamShop not found",
            "message": f"No ice cream shop found with id: {id}"
        }), 404

    new_ingredient = Ingredient(
        name=request.form['name'],
        category=request.form['category'],
        price=float(request.form['price']),
        calories=int(request.form['calories']),
        stock=int(request.form['stock']),
        vegan=request.form.get('vegan') == 'on',
        flavor=request.form.get('flavor', ''),
        id_ice_cream_shop=id
    )

    db.session.add(new_ingredient)
    db.session.commit()

    return redirect(url_for('ingredient_bp.ingredients', id=id))
