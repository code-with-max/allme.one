import urllib
import hashlib

# Set your variables here
# email = "max@deadend.xyz"
# default = "https://www.example.com/default.jpg"
# size = 40

# # construct the url
# gravatar_url = "https://www.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest() + "?"
# gravatar_url += urllib.urlencode({'d':default, 's':str(size)})


class Gravatar:
    '''
    Simple implement of gravatar service use for images
    http://en.gravatar.com/site/implement/images/
    '''
    def __init__(self: object, email: str):
        self.email = email.encode('utf-8').lower()
        self.base_url = "https://www.gravatar.com/avatar/"
        self.size = 120
        self.default = "mp"

    def get_md5(self: object) -> str:
        return hashlib.md5(self.email).hexdigest()

    def get_gravatar(self) -> str:
        # TODO Need refactor this line
        url = f'{self.base_url}{self.get_md5()}?{urllib.parse.urlencode({"d": self.default, "s": self.size})}'
        return url
