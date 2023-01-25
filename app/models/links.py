from app.extensions import db
# from app.models.user import User


class Links(db.Model):
    '''User social networks links model for SQLAlchemy'''
    # __tablename__ = links
    # may be using key "uselist=False" in relationships
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    unique_link = db.Column(db.String(12), unique=True)
    last_viewed = db.Column(db.DateTime(timezone=True))
    about = (db.relationship('About', backref='links'))
    email = (db.relationship('Email', backref='links'))
    twitter = (db.relationship('Twitter', backref='links'))
    youtube = (db.relationship('Youtube', backref='links'))
    facebook = (db.relationship('Facebook', backref='links'))
    vkontakte = (db.relationship('Vkontakte', backref='links'))
    instagram = (db.relationship('Instagram', backref='links'))
    buymeacoffe = (db.relationship('Buymeacoffe', backref='links'))
    cloudtips = (db.relationship('Cloudtips', backref='links'))
    boosty = (db.relationship('Boosty', backref='links'))
    telegram = (db.relationship('Telegram', backref='links'))
    github = (db.relationship('Github', backref='links'))
    playmarket = (db.relationship('Playmarket', backref='links'))

    def __repr__(self) -> str:
        return f'Unique link: {self.unique_link}'

    def get_link(self, req) -> object:
        '''
        Return first social link in current list of links exist
        '''
        if req == 'about' and self.about:
            return self.about[0]

        elif req == 'email' and self.email:
            return self.email[0]

        elif req == 'twitter' and self.twitter:
            return self.twitter[0]

        elif req == 'youtube' and self.twitter:
            return self.youtube[0]

        elif req == 'facebook' and self.facebook:
            return self.facebook[0]

        elif req == 'vkontakte' and self.vkontakte:
            return self.vkontakte[0]

        elif req == 'instagram' and self.instagram:
            return self.instagram[0]

        elif req == 'buymeacoffe' and self.buymeacoffe:
            return self.buymeacoffe[0]

        elif req == 'cloudtips' and self.cloudtips:
            return self.cloudtips[0]

        elif req == 'boosty' and self.boosty:
            return self.boosty[0]

        elif req == 'telegram' and self.telegram:
            return self.telegram[0]

        elif req == 'github' and self.github:
            return self.github[0]

        elif req == 'playmarket' and self.playmarket:
            return self.playmarket[0]

        else:
            return None

    def get_links(self) -> list:
        '''
        1st return [list] of first social links if it exist \n
        2nd rerurn [list] of free social links (if link not exist) \n
        The method does not use the user's payment status \n
        current_user.is_paying() - for check it
        '''
        used = []
        free = []
        used.append(self.about[0]) if self.about else free.append('about')
        used.append(self.github[0]) if self.github else free.append('github')
        used.append(self.playmarket[0]) if self.playmarket else free.append('playmarket')
        used.append(self.youtube[0]) if self.youtube else free.append('youtube')
        used.append(self.twitter[0]) if self.twitter else free.append('twitter')
        used.append(self.boosty[0]) if self.boosty else free.append('boosty')
        used.append(self.buymeacoffe[0]) if self.buymeacoffe else free.append('buymeacoffe')
        used.append(self.facebook[0]) if self.facebook else free.append('facebook')
        used.append(self.instagram[0]) if self.instagram else free.append('instagram')
        used.append(self.vkontakte[0]) if self.vkontakte else free.append('vk')
        used.append(self.cloudtips[0]) if self.cloudtips else free.append('cloudtips')
        used.append(self.email[0]) if self.email else free.append('email')
        used.append(self.telegram[0]) if self.telegram else free.append('telegram')
        return [used, free]


class SocialNetwork():
    '''
    Helper Class for implement user social networks link \n
    Requred named parameters: username \n
    '''
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(160))
    about = db.Column(db.String(32))
    network_name = db.Column(db.String(16))
    description = db.Column(db.String(255))

    def get_title(self):
        # Need capitalise first letter
        return self.network_name


class About(db.Model, SocialNetwork):
    links_id = db.Column(db.Integer, db.ForeignKey('links.id'))

    def __init__(self, **kwargs) -> None:
        super().__init__(network_name='about', **kwargs)

    def __repr__(self) -> str:
        return f'<(about) User name: {self.username}>'


class Email(db.Model, SocialNetwork):
    links_id = db.Column(db.Integer, db.ForeignKey('links.id'))

    def __init__(self, **kwargs) -> None:
        super().__init__(network_name='email', **kwargs)

    def __repr__(self) -> str:
        return f'<E-mail adress: {self.username}>'


class Twitter(db.Model, SocialNetwork):
    '''
    Base class for implement database model for user Twitter link \n
    Requred parameter: username
    '''
    links_id = db.Column(db.Integer, db.ForeignKey('links.id'))

    def __init__(self, **kwargs) -> None:
        super().__init__(network_name='twitter', **kwargs)

    def __repr__(self) -> str:
        return f'<Twitter username: {self.username}>'


class Instagram(db.Model, SocialNetwork):
    links_id = db.Column(db.Integer, db.ForeignKey('links.id'))

    def __init__(self, **kwargs) -> None:
        super().__init__(network_name='instagram', **kwargs)

    def __repr__(self) -> str:
        return f'<Instagram username: {self.username}>'


class Facebook(db.Model, SocialNetwork):
    links_id = db.Column(db.Integer, db.ForeignKey('links.id'))

    def __init__(self, **kwargs) -> None:
        super().__init__(network_name='facebook', **kwargs)

    def __repr__(self) -> str:
        return f'<Facebook username: {self.username}>'


class Vkontakte(db.Model, SocialNetwork):
    links_id = db.Column(db.Integer, db.ForeignKey('links.id'))

    def __init__(self, **kwargs) -> None:
        super().__init__(network_name='vk', **kwargs)

    def __repr__(self) -> str:
        return f'<Vkontakte username: {self.username}>'


class Youtube(db.Model, SocialNetwork):
    links_id = db.Column(db.Integer, db.ForeignKey('links.id'))

    def __init__(self, **kwargs) -> None:
        super().__init__(network_name='youtube', **kwargs)

    def __repr__(self) -> str:
        return f'<YouTube username: {self.username}>'


class Buymeacoffe(db.Model, SocialNetwork):
    links_id = db.Column(db.Integer, db.ForeignKey('links.id'))

    def __init__(self, **kwargs) -> None:
        super().__init__(network_name='buymeacoffe', **kwargs)

    def __repr__(self) -> str:
        return f'<buymeacoffe username: {self.username}>'


class Cloudtips(db.Model, SocialNetwork):
    links_id = db.Column(db.Integer, db.ForeignKey('links.id'))

    def __init__(self, **kwargs) -> None:
        super().__init__(network_name='cloudtips', **kwargs)

    def __repr__(self) -> str:
        return f'<cloudtips username: {self.username}>'


class Boosty(db.Model, SocialNetwork):
    links_id = db.Column(db.Integer, db.ForeignKey('links.id'))

    def __init__(self, **kwargs) -> None:
        super().__init__(network_name='boosty', **kwargs)

    def __repr__(self) -> str:
        return f'<boosty username: {self.username}>'


class Telegram(db.Model, SocialNetwork):
    links_id = db.Column(db.Integer, db.ForeignKey('links.id'))

    def __init__(self, **kwargs) -> None:
        super().__init__(network_name='telegram', **kwargs)

    def __repr__(self) -> str:
        return f'<telegram username: {self.username}>'


class Github(db.Model, SocialNetwork):
    links_id = db.Column(db.Integer, db.ForeignKey('links.id'))

    def __init__(self, **kwargs) -> None:
        super().__init__(network_name='github', **kwargs)

    def __repr__(self) -> str:
        return f'<github username: {self.username}>'


class Playmarket(db.Model, SocialNetwork):
    links_id = db.Column(db.Integer, db.ForeignKey('links.id'))

    def __init__(self, **kwargs) -> None:
        super().__init__(network_name='playmarket', **kwargs)

    def __repr__(self) -> str:
        return f'<playmarket username: {self.username}>'
