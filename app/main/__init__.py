from flask import Blueprint

bp = Blueprint('main', __name__)


from app.main import routes
from app.main.links import about
from app.main.links import email
from app.main.links import twitter
from app.main.links import facebook
from app.main.links import instagram
from app.main.links import youtube
from app.main.links import cloudtips
from app.main.links import buymeacoffe
from app.main.links import boosty
