from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Product(db.Model):
    id = db.Column(db.String(50), primary_key=True, unique=True)
    title = db.Column(db.String(1000), nullable=True)
    image_url = db.Column(db.String(1000), nullable=True)
    price = db.Column(db.String(25), nullable=True)
    review = db.Column(db.String(25), nullable=True)

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "image_url": self.image_url,
            "price": self.price,
            "review": self.review,
        }
