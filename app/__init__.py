from flask import Flask

from config import Config
from app.extensions import db
from app.extensions import login_manager
from app.extensions import migrate
from app.extensions import mail
from app.extensions import env


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions here
    # SQLAlchemy
    db.init_app(app)

    # Flask-Login
    from app.models.user import User
    login_manager.init_app(app)

    # Migrations
    migrate.init_app(app, db)

    # Auto-escape

    #  Flask-mail
    mail.init_app(app)

    # Register blueprints here
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.api2 import bp as api2_bp
    app.register_blueprint(api2_bp, url_prefix='/api2')

    from app.about import bp as about_bp
    app.register_blueprint(about_bp, url_prefix='/about')

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    @app.route('/test/')
    def test_page():
        return '<h1>Testing the Flask Application Factory Pattern</h1>'

    return app
