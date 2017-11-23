from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from scraper import Scraper
from models import Product, db
import os


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI", "sqlite:///../database.sqlite3")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

with app.app_context():
    db.init_app(app)
    db.create_all()

@app.route('/get-products/<keyword>')
def index(keyword):
    scraper = Scraper(keyword)
    products = scraper.get_products()

    json = {"products": [p.serialize() for p in products]}

    for p in products:
        db.session.add(p)
        db.session.commit()

    return str(json)


if __name__ == "__main__":
    app.run(debug=True)
