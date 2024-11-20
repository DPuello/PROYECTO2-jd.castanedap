from models.functions import get_best_product, bcolors
from database.db import db


class IceCreamShop(db.Model):
    __tablename__ = "ice_cream_shops"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    day_sales = db.Column(db.Integer, nullable=False, default=0)
    day_total_sold = db.Column(db.Float, nullable=False, default=0)
    products = db.relationship(
        "Product",
        backref="ice_cream_shop",
        lazy=True,
        cascade="all, delete-orphan"
    )
    ingredients = db.relationship(
        "Ingredient",
        backref="ice_cream_shop",
        lazy=True,
        cascade="all, delete-orphan"
    )

    MAX_PRODUCTS = 4  # Class constant for max products

    @property
    def can_add_product(self):
        """Check if shop can add more products"""
        return len(self.products) < self.MAX_PRODUCTS

    def create_product(self, product_data):
        """Create a new product with validation"""
        if not self.can_add_product:
            raise ValueError(f"Maximum number of products ({
                             self.MAX_PRODUCTS}) reached")

        # Create and add product logic here
        new_product = Product(
            name=product_data['name'],
            price=product_data['price'],
            category=product_data['category'],
            id_ice_cream_shop=self.id
        )
        self.products.append(new_product)
        return new_product

    def get_best_product(self):
        product_list = [{"name": product.name,
                         "earnings": product.calc_earnings()}
                        for product in self.products]
        return get_best_product(product_list)

    def sell(self, product_name: str):
        try:
            for product_to_sell in self.products:
                if product_name in product_to_sell.name:
                    break
            else:
                raise ValueError("Product not found")

            # Find the insufficient ingredient first
            insufficient_ingredient = next(
                (ing for ing in product_to_sell.ingredients if not ing.is_enough_stock()),
                None
            )
            if insufficient_ingredient:
                raise ValueError(
                    f"Oh no! Ingredient {insufficient_ingredient.name} insufficient ☹️")

            for ingredient in product_to_sell.ingredients:
                ingredient.spend()

            self.day_sales += 1
            self.day_total_sold += product_to_sell.price
            return True
        except Exception as e:
            return str(e)

    def sell_product(self, product):
        try:
            index = int(product) - 1
            if index < 0 or index >= len(self.products):
                return
            return self.sell(self.products[index].name)
        except ValueError:
            return self.sell(product)
