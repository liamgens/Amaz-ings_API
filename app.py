from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from scraper import Scraper

app = Flask(__name__)
db = SQLAlchemy(app)

@app.route('/get-products/<keyword>')
def index(keyword):
    scraper = Scraper(keyword)
    products = scraper.get_products()

    json = {"products": []}

    for product in products:
        p = Product()
        p.id = product[0]
        p.title = product[1]
        p.image_url = product[2]
        p.price = product[3]
        p.review = product[4]
        json["products"].append(p.serialize())

    return str(json)


class Product(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    title = db.Column(db.String(1000), nullable=False)
    image_url = db.Column(db.String(1000))
    price = db.Column(db.String(25), nullable=False)
    review = db.Column(db.String(25))

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "image_url": self.image_url,
            "price": self.price,
            "review": self.review,
        }


if __name__ == "__main__":
    app.run(debug=True)
