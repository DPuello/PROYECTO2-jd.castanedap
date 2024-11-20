from models.product import Product
from models.icecreamshop import IceCreamShop
from models.ingredient import Ingredient
from database.db import db
from flask import (
    Blueprint, jsonify, render_template,
    request, redirect, url_for
)

product_blueprint = Blueprint("product_bp", __name__)


@product_blueprint.route("/products")
def index():
    products = Product.query.all()
    return render_template("all_products.html", products=products)


@product_blueprint.route("/<id>/products")
def products(id):
    icecreamshop = IceCreamShop.query.filter_by(id=id).first()
    if icecreamshop is None:
        return jsonify({
            "error": "IceCreamShop not found",
            "message": f"No ice cream shop found with id: {id}"
        }), 404
    return render_template(
        "products.html",
        products=icecreamshop.products,
        icecreamshop=icecreamshop
    )


@product_blueprint.route("/<id>/products/new")
def new(id):
    icecreamshop = IceCreamShop.query.filter_by(id=id).first()
    if icecreamshop is None:
        return jsonify({
            "error": "IceCreamShop not found",
            "message": f"No ice cream shop found with id: {id}"
        }), 404

    if not icecreamshop.can_add_product:
        return jsonify({
            "error": "Maximum products reached",
            "message": f"Maximum number of products ({IceCreamShop.MAX_PRODUCTS}) reached"
        }), 400

    return render_template(
        "new_product.html",
        icecreamshop=icecreamshop
    )


@product_blueprint.route("/<id>/products/create", methods=["POST"])
def create(id):
    icecreamshop = IceCreamShop.query.filter_by(id=id).first()
    if icecreamshop is None:
        return jsonify({
            "error": "IceCreamShop not found",
            "message": f"No ice cream shop found with id: {id}"
        }), 404

    if not icecreamshop.can_add_product:
        return jsonify({
            "error": "Maximum products reached",
            "message": f"Maximum number of products ({IceCreamShop.MAX_PRODUCTS}) reached"
        }), 400

    form_data = {
        'name': request.form['name'],
        'price': float(request.form['price']),
        'category': request.form['category'],
        'ingredients': request.form.getlist('ingredients'),
    }

    try:
        new_product = Product(
            name=form_data['name'],
            price=form_data['price'],
            category=form_data['category'],
            id_ice_cream_shop=id,
        )

        ingredient_ids = [int(id) for id in form_data['ingredients']]
        ingredients = Ingredient.query.filter(
            Ingredient.id.in_(ingredient_ids)).all()
        new_product.ingredients.extend(ingredients)

        db.session.add(new_product)
        db.session.commit()
        return redirect(url_for('product_bp.products', id=id))
    except ValueError as e:
        return str(e), 400


@product_blueprint.route("/<id>/sell/<name>")
def sell(id, name):
    icecreamshop = IceCreamShop.query.filter_by(id=id).first()
    if icecreamshop is None:
        return jsonify({
            "error": "IceCreamShop not found",
            "message": f"No ice cream shop found with id: {id}"
        }), 404

    result = icecreamshop.sell(name)
    if result is True:
        db.session.commit()
        return jsonify({"success": True, "message": f"Sold product!: {name}"})
    else:
        return jsonify({
            "success": False,
            "error": "Error selling product",
            "message": result
        }), 400


@product_blueprint.route("/products/calculate_calories/<id>")
def calculate_calories(id):
    product = Product.query.filter_by(id=id).first()
    if product is None:
        return jsonify({
            "error": "Product not found",
            "message": f"No product found with id: {id}"
        }), 404
    return f"Calories: {product.calc_calories()}"


@product_blueprint.route("/products/calculate_cost/<id>")
def calculate_cost(id):
    product = Product.query.filter_by(id=id).first()
    if product is None:
        return jsonify({
            "error": "Product not found",
            "message": f"No product found with id: {id}"
        }), 404
    return f"Cost: {product.calc_cost()}"


@product_blueprint.route("/products/calculate_earnings/<id>")
def calculate_earnings(id):
    product = Product.query.filter_by(id=id).first()
    if product is None:
        return jsonify({
            "error": "Product not found",
            "message": f"No product found with id: {id}"
        }), 404
    return f"Earnings: {product.calc_earnings()}"
