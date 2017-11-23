from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


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
