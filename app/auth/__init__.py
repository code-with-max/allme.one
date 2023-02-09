from flask import Blueprint
# FIXME Maybe better using apllication layer for URLSafeTimedSerializer
from itsdangerous import URLSafeTimedSerializer
from config import Config


bp = Blueprint('auth', __name__)
s = URLSafeTimedSerializer(Config.URL_STS_KEY)


from app.auth import routes
from app.auth.utility import send_verification_email
from app.auth.utility import confirm_required
