import uuid
import random
from sqlalchemy.sql import func
from app.extensions import db


class Apikey(db.Model):
    __tablename__ = 'api_key'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(16))
    key = db.Column(db.String(32), unique=True)
    count = db.Column(db.Integer, default=0)
    coun2 = db.Column(db.Integer, default=0)  # FIXME Delete this row
    last_used = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    def __init__(self, *args, **kwargs) -> None:
        colours = ["Red", "Golden", "Blue", "Purple", "White", "Silver"]
        animals = ["Lion", "Dragon", "Unicorn", "Horse", "Tiger"]
        gname = f'{random.choice(colours)}-{random.choice(animals)}'
        gkey = uuid.uuid4().hex
        super().__init__(name=gname, key=gkey, count=0, *args, **kwargs)

    def increase(self) -> int:
        # Not works. Not used :(
        self.count += 1
        db.session.add(self.count)
        db.session.commit()
        return self.count

    def last_used_update(self):
        self.last_used = func.now()

    def __repr__(self) -> str:
        return f'{self.name}: used:{self.count} times. KEY: {self.key}'
