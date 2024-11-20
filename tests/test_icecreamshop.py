import unittest
from app import app
from database.db import db
from models.ingredient import Ingredient
from models.product import Product
from models.icecreamshop import IceCreamShop


class TestIceCreamShop(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

            # Create Ice Cream Shop first
            shop = IceCreamShop(name="Test Shop")
            db.session.add(shop)
            db.session.commit()

            # Store shop ID for later use
            self.shop_id = shop.id

            # Create test ingredients
            ingredients = [
                Ingredient(
                    name="Milk",
                    price=1000,
                    calories=100,
                    stock=10,
                    vegan=False,
                    category="Base",
                    id_ice_cream_shop=self.shop_id
                ),
                Ingredient(
                    name="Cream",
                    price=1500,
                    calories=150,
                    stock=8,
                    vegan=False,
                    category="Base",
                    id_ice_cream_shop=self.shop_id
                ),
                Ingredient(
                    name="Chocolate",
                    price=2000,
                    calories=200,
                    stock=15,
                    vegan=True,
                    category="Base",
                    id_ice_cream_shop=self.shop_id
                ),
                Ingredient(
                    name="Vanilla Extract",
                    price=3000,
                    calories=50,
                    stock=2,
                    vegan=True,
                    category="Complement",
                    id_ice_cream_shop=self.shop_id
                ),
            ]

            for ingredient in ingredients:
                db.session.add(ingredient)
            db.session.commit()

            # Create test products
            vanilla_milkshake = Product(
                name="Classic Vanilla Milkshake",
                category="Milkshake",
                price=9000,
                id_ice_cream_shop=self.shop_id
            )
            vanilla_milkshake.ingredients.extend(ingredients)

            vanilla_cup = Product(
                name="Classic Vanilla Cup",
                category="Cup",
                price=10000,
                id_ice_cream_shop=self.shop_id
            )
            vanilla_cup.ingredients.extend(ingredients)

            db.session.add(vanilla_milkshake)
            db.session.add(vanilla_cup)
            db.session.commit()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_get_best_product(self):
        with app.app_context():
            response = self.app.get(f"/{self.shop_id}/best_product")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                response.data.decode("utf-8"),
                "Classic Vanilla Cup"
            )

            response2 = self.app.get("/1000/best_product")
            self.assertEqual(response2.status_code, 404)
            self.assertEqual(response2.json.get("error"),
                             "IceCreamShop not found")

    def test_product_sell(self):
        with app.app_context():
            response = self.app.get(
                f"/{self.shop_id}/sell/Classic Vanilla Cup")
            shop = IceCreamShop.query.filter_by(id=self.shop_id).first()
            self.assertEqual(response.status_code, 200)
            self.assertEqual(shop.day_sales, 1)
            self.assertEqual(shop.day_total_sold, 10000)
            self.assertEqual(shop.ingredients[0].stock, 9.8)
            self.assertEqual(shop.ingredients[3].stock, 1.0)
            self.assertEqual(response.json.get("message"),
                             "Sold product!: Classic Vanilla Cup")

            response2 = self.app.get(
                f"/{self.shop_id}/sell/Classic Vanilla Milkshake")
            shop = IceCreamShop.query.filter_by(id=self.shop_id).first()
            self.assertEqual(response2.status_code, 200)
            self.assertEqual(shop.day_sales, 2)
            self.assertEqual(shop.day_total_sold, 19000)
            self.assertEqual(shop.ingredients[0].stock, 9.6)
            self.assertEqual(shop.ingredients[3].stock, 0.0)
            self.assertEqual(response2.json.get("message"),
                             "Sold product!: Classic Vanilla Milkshake")

            response3 = self.app.get(
                f"/{self.shop_id}/sell/Classic Undefined Product")
            self.assertEqual(response3.status_code, 400)
            self.assertEqual(response3.json.get("message"),
                             "Product not found")

            response4 = self.app.get(
                f"/{self.shop_id}/sell/Classic Vanilla Cup")
            self.assertEqual(response4.status_code, 400)
            self.assertEqual(response4.json.get("message"),
                             "Ingredient Vanilla Extract insufficient")

            response5 = self.app.get("/1000/sell/Classic Vanilla Cup")
            self.assertEqual(response5.status_code, 404)
            self.assertEqual(response5.json.get("error"),
                             "IceCreamShop not found")
