from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from scraper import Scraper
from models import Product, db

app = Flask(__name__)
db.init_app(app)


@app.route('/get-products/<keyword>')
def index(keyword):
    scraper = Scraper(keyword)
    products = scraper.get_products()

    json = {"products": []}

    for product in products:
        json["products"].append(product.serialize())

    return str(json)


if __name__ == "__main__":
    app.run(debug=True)
