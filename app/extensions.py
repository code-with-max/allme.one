from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


from flask_login import LoginManager
login_manager = LoginManager()


from flask_migrate import Migrate
migrate = Migrate()


from flask_mail import Mail
mail = Mail()


from jinja2 import Environment, select_autoescape
env = Environment(
        autoescape=select_autoescape(
            enabled_extensions=('html', 'xml'),
            default_for_string=True,
            )
        )
