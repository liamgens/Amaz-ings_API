from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from scraper import Scraper
from models import Product, db
from datetime import datetime, timedelta
import config


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI

with app.app_context():
    db.init_app(app)
    db.create_all()

@app.route('/get-products/<keyword>')
def index(keyword):
    scraper = Scraper(keyword)

    products = Product.query.filter_by(keyword=keyword).all()

    if len(products) < 1: # If the products DNE
        products = add_products(scraper)

    elif (datetime.utcnow() - products[0].updated) > timedelta(1): # If the products are over 24 hours old
        products = add_products(scraper)

    json = {keyword: [p.serialize() for p in products]}

    return str(json)

def add_products(scraper):
    products = scraper.get_products()

    for p in products:
        db.session.add(p)
        db.session.commit()

    return products


if __name__ == "__main__":
    app.run(debug=True)
