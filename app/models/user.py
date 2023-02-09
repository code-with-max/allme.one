import uuid
from flask_login import UserMixin
from sqlalchemy.sql import func
from app.extensions import db


class User(db.Model, UserMixin):
    # __tablename__ = user
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(160), unique=True)
    email_confirmed = db.Column(db.Boolean, default=False)
    password = db.Column(db.String(160))
    created_date = db.Column(db.DateTime(timezone=True), default=func.now())
    last_visit = db.Column(db.DateTime(timezone=True))
    payment_state = db.Column(db.String(12), default='white')
    payment_period = db.Column(db.String(12))
    payment_date = db.Column(db.DateTime(timezone=True))
    payment_UUID = db.Column(db.String(36), unique=True)
    API_key = db.Column(db.String(12))
    API_counter = db.Column(db.Integer, default=0)
    links = db.relationship('Links', backref='user', cascade='all, delete-orphan')

    def __init__(self, *args, **kwargs):
        self.payment_UUID = uuid.uuid4()
        super().__init__(*args, **kwargs)

    def __repr__(self) -> str:
        return f'<e-mail: "{self.email}", user_links: {self.links}>'

    def is_paying(self: object) -> bool:
        ''' Return boolean user payment status'''
        if self.payment_state != 'white':
            return True
        else:
            return False

    def get_list(self) -> object:
        ''' Return first list of links from data base '''
        return self.links[0]
