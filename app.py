import os
from dotenv import load_dotenv
from flask import Flask
from database.db import db, init_db
from controllers.icecreamshop_controller import icecreamshop_blueprint
from controllers.ingredient_controller import ingredient_blueprint
from controllers.product_controller import product_blueprint

load_dotenv()
app = Flask(__name__, template_folder="views")
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{os.getenv("DB_USERNAME")}:{os.getenv(
    "DB_PASSWORD")}@{os.getenv("DB_HOST")}:{os.getenv("DB_PORT")}/{os.getenv("DB_NAME")}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
# uncomment to reset db data
init_db(app)
app.register_blueprint(icecreamshop_blueprint)
app.register_blueprint(ingredient_blueprint)
app.register_blueprint(product_blueprint)

if __name__ == "__main__":
    app.run(debug=True)
