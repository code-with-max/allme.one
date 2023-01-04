from app.extensions import db
# from app.models.user import User


class Links(db.Model):
    # __tablename__ = links
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    unique_link = db.Column(db.String(12), unique=True)
    about = (db.relationship('About', backref='links'))
    email = (db.relationship('Email', backref='links'))
    twitter = (db.relationship('Twitter', backref='links'))
    facebook = (db.relationship('Facebook', backref='links'))
    vkontakte = (db.relationship('Vkontakte', backref='links'))

    def __repr__(self) -> str:
        return f'Unique link: {self.unique_link}'


class About(db.Model):
    # __tablename__ = about
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), default='You name')
    description = db.Column(db.String(255), default='Tell something about you')
    links_id = db.Column(db.Integer, db.ForeignKey('links.id'))

    def __repr__(self) -> str:
        return f'<User name: {self.name}>'


class Email(db.Model):
    # __tablename__ = email
    id = db.Column(db.Integer, primary_key=True)
    adress = db.Column(db.String(160), default="no@one.ru")
    description = db.Column(db.String(255))
    links_id = db.Column(db.Integer, db.ForeignKey('links.id'))

    def __repr__(self) -> str:
        return f'<E-mail adress: {self.adress}>'


class Twitter(db.Model):
    # __tablename__ = twitter
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(160))
    links_id = db.Column(db.Integer, db.ForeignKey('links.id'))

    def __repr__(self) -> str:
        return f'<Username: {self.username}>'


class Facebook(db.Model):
    # __tablename__ = facebook
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(160))
    links_id = db.Column(db.Integer, db.ForeignKey('links.id'))

    def __repr__(self) -> str:
        return f'<Username: {self.username}>'


class Vkontakte(db.Model):
    # __tablename__ = vkontakte
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(160))
    links_id = db.Column(db.Integer, db.ForeignKey('links.id'))

    def __repr__(self) -> str:
        return f'<Username: {self.username}>'
