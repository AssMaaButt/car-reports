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

    # Initialize extensions with the app
    db.init_app(app)
    jwt.init_app(app)
    ma.init_app(app)

    # Register blueprints (routes)
    from app.routes import main_bp
    from app.routes.auth_routes import auth_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)

    return app
