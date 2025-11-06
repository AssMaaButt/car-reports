from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from config import Config

# Initialize extensions
db = SQLAlchemy()
jwt = JWTManager()
ma = Marshmallow()

def create_app():
    """Application factory pattern."""
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    ma.init_app(app)

    # Register blueprints (web)
    from app.web import main_bp
    from app.web.users.api import users_bp
    from app.web.cars.api import cars_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(cars_bp)

    return app
