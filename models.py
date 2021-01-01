"""Models for Cupcake app."""
from flask_sqlalchemy import SQLAlchemy

GENERAL_IMAGE = "https://static7.depositphotos.com/1172692/731/v/600/depositphotos_7319827-stock-illustration-vector-sweet-retro-cupcake-button.jpg"

db = SQLAlchemy()

def connect_db(app):
    """Connect this database with the provided flask app"""
    db.app= app
    db.init_app(app)

class Cupcake(db.Model):
    __tablename__ = 'cupcake'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    flavor = db.Column(db.String(50), nullable = False)
    size = db.Column(db.String(50), nullable = False)
    rating = db.Column(db.Float, nullable = False)
    image = db.Column(db.String(150), nullable = False, default = GENERAL_IMAGE)

    def image_url(self):
        """Set image link with a default link if no link exists"""
        return self.image or GENERAL_IMAGE