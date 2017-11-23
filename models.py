from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Product(db.Model):
    keyword = db.Column(db.String(100), primary_key=True)
    id = db.Column(db.String(50), primary_key=True)
    title = db.Column(db.String(1000), nullable=True)
    image_url = db.Column(db.String(1000), nullable=True)
    price = db.Column(db.String(25), nullable=True)
    review = db.Column(db.String(25), nullable=True)
    updated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "image_url": self.image_url,
            "price": self.price,
            "review": self.review,
        }

    def is_none(self):
        return True if self.keyword is None or self.id is None or self.title is None or self.price is None or self.review is None else False

    def __eq__(self, other):
        return (self.keyword, self.id) == (other.keyword, other.id)

    def __hash__(self):
        return (self.keyword, self.id).__hash__()
