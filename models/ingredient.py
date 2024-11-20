from models.functions import is_healthy
from database.db import db


class Ingredient(db.Model):
    __tablename__ = "ingredients"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False, default=800)
    calories = db.Column(db.Integer, nullable=False, default=0)
    stock = db.Column(db.Float, nullable=False, default=5)
    vegan = db.Column(db.Boolean, nullable=False, default=False)
    category = db.Column(db.String(100), nullable=False, default="Base")
    flavor = db.Column(db.String(100), default=None)
    id_ice_cream_shop = db.Column(db.Integer, db.ForeignKey(
        "ice_cream_shops.id"), nullable=False)

    def its_healthy(self) -> bool:
        return is_healthy(self.calories, self.vegan)

    def is_enough_stock(self):
        if self.category == "Base":
            return self.stock >= 0.2
        else:
            return self.stock >= 1

    def spend(self):
        if self.stock > 0:
            if self.category == "Base":
                self.stock -= 0.2
            else:
                self.stock -= 1
            return True
        return False

    def stock_up(self) -> None:
        if self.category == "Base":
            self.stock += 5
        else:
            self.stock += 10

    def renew_stock(self) -> None:
        if self.category == "Complement":
            self.stock = 0
        else:
            raise ValueError("Base ingredients cannot be renewed")
