from flask import Flask

from config import Config
from app.extensions import db
from app.extensions import login_manager
from app.extensions import migrate


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

    # Register blueprints here
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    @app.route('/test/')
    def test_page():
        return '<h1>Testing the Flask Application Factory Pattern</h1>'

    return app
