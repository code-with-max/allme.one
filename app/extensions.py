from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


from flask_login import LoginManager
login_manager = LoginManager()


from flask_migrate import Migrate
migrate = Migrate()
