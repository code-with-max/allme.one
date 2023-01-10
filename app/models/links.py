from app.extensions import db
# from app.models.user import User


class Links(db.Model):
    '''User social networks links model for SQLAlchemy'''
    # __tablename__ = links
    # may be using key "uselist=False" in relationships
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    unique_link = db.Column(db.String(12), unique=True)
    about = (db.relationship('About', backref='links'))
    email = (db.relationship('Email', backref='links'))
    twitter = (db.relationship('Twitter', backref='links'))
    facebook = (db.relationship('Facebook', backref='links'))
    vkontakte = (db.relationship('Vkontakte', backref='links'))
    instagram = (db.relationship('Instagram', backref='links'))

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

        elif req == 'facebook' and self.facebook:
            return self.facebook[0]

        elif req == 'vkontakte' and self.vkontakte:
            return self.vkontakte[0]

        elif req == 'instagram' and self.instagram:
            return self.instagram[0]
        else:
            return None

    def get_links(self):
        '''
        Return [list] of first social links if it exist \n
        The method does not use the user's payment status. To check it, use: \n
        current_user.is_paying() - for check user payment status \n
        '''
        used = []
        free = []
        used.append(self.about[0]) if self.about else free.append('about')
        used.append(self.email[0]) if self.email else free.append('email')
        used.append(self.twitter[0]) if self.twitter else free.append('twitter')
        used.append(self.facebook[0]) if self.facebook else free.append('facebook')
        used.append(self.vkontakte[0]) if self.vkontakte else free.append('vkontakte')
        used.append(self.instagram[0]) if self.instagram else free.append('instagram')
        return [used, free]

    def get_links_str(self):
        '''
        Return two list of social link in current list \n
        1st - list of string of used social links (add user data); \n
        2nd - list of strings of avaible social links (no user data);
        '''
        used = []
        free = []
        used.append('about') if self.about else free.append('about')
        used.append('email') if self.email else free.append('email')
        used.append('twitter') if self.twitter else free.append('twitter')
        used.append('facebook') if self.facebook else free.append('facebook')
        used.append('vkontakte') if self.vkontakte else free.append('vkontakte')
        used.append('instagram') if self.vkontakte else free.append('instagram')
        return [used, free]


class SocialNetwork():
    '''
    Helper Class for implement user social networks link \n
    Requred named parameters:
    username
    network_name
    '''
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(160))
    network_name = db.Column(db.String(16))
    description = db.Column(db.String(255), default='Tell something about')

    def get_title(self):
        # Need capitalise first letter
        return self.network_name


class About(db.Model, SocialNetwork):
    links_id = db.Column(db.Integer, db.ForeignKey('links.id'))

    def __init__(self, **kwargs) -> None:
        super().__init__(network_name='about', **kwargs,)

    def __repr__(self) -> str:
        return f'<User name: {self.username}>'


class Email(db.Model, SocialNetwork):
    adress = db.Column(db.String(160), default="no@one.ru")
    links_id = db.Column(db.Integer, db.ForeignKey('links.id'))

    def __init__(self, **kwargs) -> None:
        super().__init__(network_name='email', **kwargs,)

    def __repr__(self) -> str:
        return f'<E-mail adress: {self.adress}>'


class Twitter(db.Model, SocialNetwork):
    '''
    Base class for implement database model for user Twitter link \n
    Requred parameter: username
    '''
    links_id = db.Column(db.Integer, db.ForeignKey('links.id'))

    def __init__(self, **kwargs) -> None:
        super().__init__(network_name='twitter', **kwargs,)

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
        super().__init__(network_name='vkontakte', **kwargs)

    def __repr__(self) -> str:
        return f'<Vkontakte username: {self.username}>'
