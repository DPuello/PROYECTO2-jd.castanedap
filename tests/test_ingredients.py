import unittest
from app import app
from database.db import db, init_db
from models.ingredient import Ingredient


class TestIngredient(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
        with app.app_context():
            init_db(app)
            self.app.testing = True

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_is_healthy(self):
        with app.app_context():
            # Create test ingredients
            ingredient = Ingredient(
                name="Milk",
                price=1000,
                calories=100,
                stock=10,
                vegan=False,
                id_ice_cream_shop=1  # Add required foreign key
            )
            ingredient2 = Ingredient(
                name="Sugar",
                price=1000,
                calories=100,
                stock=10,
                vegan=True,
                id_ice_cream_shop=1  # Add required foreign key
            )

            # Add and commit to database
            db.session.add(ingredient)
            db.session.add(ingredient2)
            db.session.commit()

            # Test first ingredient
            response = self.app.get(f"/ingredients/{ingredient.id}/is_healthy")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                response.data.decode("utf-8"),
                "Is healthy: False"
            )

            # Test second ingredient
            response2 = self.app.get(
                f"/ingredients/{ingredient2.id}/is_healthy")
            self.assertEqual(response2.status_code, 200)
            self.assertEqual(
                response2.data.decode("utf-8"),
                "Is healthy: True"
            )

            response3 = self.app.get("/ingredients/1000/is_healthy")
            self.assertEqual(response3.status_code, 404)
            self.assertEqual(response3.json.get("error"),
                             "Ingredient not found")

    def test_stock_up(self):
        with app.app_context():
            ingredient = Ingredient(
                name="Milk",
                price=1000,
                calories=100,
                stock=10,
                vegan=False,
                category="Base",
                id_ice_cream_shop=1
            )
            ingredient2 = Ingredient(
                name="Sugar",
                price=1000,
                calories=100,
                stock=10,
                vegan=True,
                category="Complement",
                id_ice_cream_shop=1
            )
            db.session.add(ingredient)
            db.session.add(ingredient2)
            db.session.commit()

            response = self.app.get(
                f"/{ingredient.id_ice_cream_shop}/stock/{ingredient.id}")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(ingredient.stock, 15)

            response2 = self.app.get(
                f"/{ingredient2.id_ice_cream_shop}/stock/{ingredient2.id}")
            self.assertEqual(response2.status_code, 200)
            self.assertEqual(ingredient2.stock, 20)

            response3 = self.app.get(
                f"/{ingredient.id_ice_cream_shop}/stock/1000")
            self.assertEqual(response3.status_code, 404)
            self.assertEqual(response3.json.get("error"),
                             "Ingredient not found")

    def test_renew_stock(self):
        with app.app_context():
            ingredient = Ingredient(
                name="Milk",
                price=1000,
                calories=100,
                stock=10,
                vegan=False,
                category="Base",
                id_ice_cream_shop=1
            )
            ingredient2 = Ingredient(
                name="Sugar",
                price=1000,
                calories=100,
                stock=10,
                vegan=True,
                category="Complement",
                id_ice_cream_shop=1
            )
            db.session.add(ingredient)
            db.session.add(ingredient2)
            db.session.commit()

            response = self.app.get(
                f"/{ingredient.id_ice_cream_shop}/renew/{ingredient.id}")
            self.assertEqual(
                response.json.get("error"),
                "Base ingredients cannot be renewed"
            )

            response2 = self.app.get(
                f"/{ingredient2.id_ice_cream_shop}/renew/{ingredient2.id}")
            self.assertEqual(response2.status_code, 200)
            self.assertEqual(ingredient2.stock, 0)

            response3 = self.app.get(
                f"/{ingredient2.id_ice_cream_shop}/renew/1000")
            self.assertEqual(response3.status_code, 404)
            self.assertEqual(response3.json.get("error"),
                             "Ingredient not found")
