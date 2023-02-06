from flask import Blueprint

bp = Blueprint('paywall', __name__)


from app.paywall import routes
