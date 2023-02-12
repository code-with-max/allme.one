import uuid
from flask_login import UserMixin
from sqlalchemy.sql import func
from app.extensions import db


class User(db.Model, UserMixin):
    '''
    Base User implementing model

    to set 'payment_state' use:
    'white': free
    'silver': user is payd
    '''
    # __tablename__ = user
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(160), unique=True)
    email_confirmed = db.Column(db.Boolean, default=False)
    password = db.Column(db.String(160))
    created_date = db.Column(db.DateTime(timezone=True), default=func.now())
    last_visit = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    payment_state = db.Column(db.String(12), default='white')
    payment_period = db.Column(db.String(12))
    payment_date = db.Column(db.DateTime(timezone=True))
    payment_UUID = db.Column(db.String(36), unique=True)
    links = db.relationship('Links', backref='user', cascade='all, delete-orphan')
    api_keys = db.relationship('Apikey', backref='user', cascade='all, delete-orphan')

    def __init__(self, *args, **kwargs):
        pUUID = uuid.uuid4()
        super().__init__(payment_UUID=pUUID, *args, **kwargs)

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

    def update_payment_status(self, product_id: str) -> bool:
        if product_id == 'SKU_02':  # TODO move product code to other list
            self.payment_state = 'silver'
            self.payment_period = 'year'
            self.payment_date = func.now()
            return True  # FIXME may be need commit db session here
        elif product_id == 'SKU_03':
            self.payment_state = 'silver'
            self.payment_period = 'month'
            self.payment_date = func.now()
            return True
        else:
            return False
