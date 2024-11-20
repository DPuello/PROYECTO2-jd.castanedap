from database.db import db
from models.ingredient import Ingredient
from models.functions import calc_cost, calc_product_earnings, calc_calories, calc_milkshake_calories, calc_cup_cost, calc_cup_earnings

# Association table for the many-to-many relationship
product_ingredients = db.Table('product_ingredients',
                               db.Column('product_id', db.Integer, db.ForeignKey(
                                   'products.id'), primary_key=True),
                               db.Column('ingredient_id', db.Integer, db.ForeignKey(
                                   'ingredients.id'), primary_key=True)
                               )


class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    id_ice_cream_shop = db.Column(db.Integer, db.ForeignKey(
        'ice_cream_shops.id'), nullable=False)

    # Many-to-many relationship with ingredients (max 4)
    ingredients = db.relationship('Ingredient',
                                  secondary='product_ingredients',
                                  backref=db.backref('products', lazy=True),
                                  lazy=True)

    def calc_cost(self) -> float:
        cost_list = [{"name": ingredient.name, "price": ingredient.price}
                     for ingredient in self.ingredients]
        if self.category == "Cup":
            return calc_cup_cost(cost_list)
        else:
            return calc_cost(cost_list)

    def calc_earnings(self) -> float:
        cost_list = [{"name": ingredient.name, "price": ingredient.price}
                     for ingredient in self.ingredients]
        if self.category == "Cup":
            return calc_cup_earnings(self.price, cost_list)
        else:
            return calc_product_earnings(self.price, cost_list)

    def calc_calories(self) -> int:
        calories_list = [
            ingredient.calories for ingredient in self.ingredients]
        if self.category == "Cup":
            return calc_calories(calories_list)
        else:
            return calc_milkshake_calories(calories_list)
