import os
from flask import Blueprint

bp = Blueprint('paywall', __name__)


from app.paywall import routes
from app.paywall import utility
