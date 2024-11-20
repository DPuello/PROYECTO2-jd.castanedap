import unittest
from app import app
from database.db import db
from models.product import Product
from models.ingredient import Ingredient
from models.icecreamshop import IceCreamShop


class TestProduct(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

            # Create Ice Cream Shop first
            self.shop = IceCreamShop(name="Test Shop")
            db.session.add(self.shop)
            db.session.commit()

            # Create test ingredients
            ingredients = [
                Ingredient(
                    name="Milk",
                    price=1000,
                    calories=100,
                    stock=10,
                    vegan=False,
                    category="Base",
                    id_ice_cream_shop=self.shop.id
                ),
                Ingredient(
                    name="Cream",
                    price=1500,
                    calories=150,
                    stock=8,
                    vegan=False,
                    category="Base",
                    id_ice_cream_shop=self.shop.id
                ),
                Ingredient(
                    name="Chocolate",
                    price=2000,
                    calories=200,
                    stock=15,
                    vegan=True,
                    category="Base",
                    id_ice_cream_shop=self.shop.id
                ),
                Ingredient(
                    name="Vanilla Extract",
                    price=3000,
                    calories=50,
                    stock=12,
                    vegan=True,
                    category="Complement",
                    id_ice_cream_shop=self.shop.id
                ),
            ]

            for ingredient in ingredients:
                db.session.add(ingredient)
            db.session.commit()

            # Create test products
            vanilla_milkshake = Product(
                name="Classic Vanilla",
                category="Milkshake",
                price=9000,
                id_ice_cream_shop=self.shop.id
            )
            vanilla_milkshake.ingredients.extend(ingredients)

            vanilla_cup = Product(
                name="Classic Vanilla",
                category="Cup",
                price=10000,
                id_ice_cream_shop=self.shop.id
            )
            vanilla_cup.ingredients.extend(ingredients)

            db.session.add(vanilla_milkshake)
            db.session.add(vanilla_cup)
            db.session.commit()

            # Store IDs for later use
            self.milkshake_id = vanilla_milkshake.id
            self.cup_id = vanilla_cup.id

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_calculate_calories(self):
        with app.app_context():
            response = self.app.get(
                f"/products/calculate_calories/{self.milkshake_id}"
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data.decode(), "Calories: 700")

            response2 = self.app.get(
                f"/products/calculate_calories/{self.cup_id}"
            )
            self.assertEqual(response2.status_code, 200)
            self.assertEqual(response2.data.decode(), "Calories: 475")

            response3 = self.app.get("/products/calculate_calories/1000")
            self.assertEqual(response3.status_code, 404)
            self.assertEqual(response3.json.get("error"),
                             "Product not found")

    def test_calculate_cost(self):
        with app.app_context():
            response = self.app.get(
                f"/products/calculate_cost/{self.milkshake_id}"
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data, b"Cost: 7500.0")

            response2 = self.app.get(
                f"/products/calculate_cost/{self.cup_id}"
            )
            self.assertEqual(response2.status_code, 200)
            self.assertEqual(response2.data, b"Cost: 8000.0")

            response3 = self.app.get("/products/calculate_cost/1000")
            self.assertEqual(response3.status_code, 404)
            self.assertEqual(response3.json.get("error"),
                             "Product not found")

    def test_calculate_earnings(self):
        with app.app_context():
            response = self.app.get(
                f"/products/calculate_earnings/{self.milkshake_id}"
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data, b"Earnings: 1500.0")

            response2 = self.app.get(
                f"/products/calculate_earnings/{self.cup_id}"
            )
            self.assertEqual(response2.status_code, 200)
            self.assertEqual(response2.data, b"Earnings: 2000.0")

            response3 = self.app.get("/products/calculate_earnings/1000")
            self.assertEqual(response3.status_code, 404)
            self.assertEqual(response3.json.get("error"),
                             "Product not found")
