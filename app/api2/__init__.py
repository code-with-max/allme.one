from flask import Blueprint

bp = Blueprint('api2', __name__)


from app.api2 import routes
