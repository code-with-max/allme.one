from flask_login import UserMixin
from sqlalchemy.sql import func
from app.extensions import db


class User(db.Model, UserMixin):
    # __tablename__ = user
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(160), unique=True)
    password = db.Column(db.String(160))
    created_date = db.Column(db.DateTime(timezone=True), default=func.now())
    payment_state = db.Column(db.String(12), default='white')
    # unique_link = db.Column(db.String(12), unique=True)
    links = db.relationship('Links', backref='user')

    def __repr__(self):
        return f'<e-mail: "{self.email}", user_links: {self.links}>'
