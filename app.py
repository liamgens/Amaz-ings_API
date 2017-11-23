from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from scraper import Scraper
from models import Product, db
from datetime import datetime, timedelta
import config
from time import sleep
from random import randint


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

with app.app_context():
    db.init_app(app)
    db.create_all()

@app.route('/get-products/<keyword>/')
def index(keyword):
    scraper = Scraper(keyword)

    products = Product.query.filter_by(keyword=keyword).all()

    if not products: # If the products DNE
        products = add_products(scraper)

    elif (datetime.utcnow() - products[0].updated) > timedelta(1): # If the products are over 24 hours old
        for p in products: # Delete all the exisiting products
            db.session.delete(p)
            db.session.commit()
        products = add_products(scraper)

    json = {keyword: [p.serialize() for p in products]}

    return str(json)

def add_products(scraper):
    products = []

    for i in range(1, 5): # get for the first 4 pages
        sleep(randint(1,6)) # sleep for random time, between 1-5 secs, to outsmart amazon
        scraper.fetch_webpage(i)
        scraper.get_results()
        products.extend(scraper.get_products())

    products = list(set(products)) # remove any duplicate products

    for p in products:
        db.session.add(p)
        db.session.commit()

    return products


if __name__ == "__main__":
    app.run(debug=True)
