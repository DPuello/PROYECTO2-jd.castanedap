from flask_sqlalchemy import SQLAlchemy
from database.init_db import create_db_data


db = SQLAlchemy()


def init_db(app):
    with app.app_context():
        create_db_data(db)
