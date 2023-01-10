from flask import Blueprint

bp = Blueprint('main', __name__)


from app.main import routes
from app.main.links import twitter
from app.main.links import facebook
from app.main.links import instagram
