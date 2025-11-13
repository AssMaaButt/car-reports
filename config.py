import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Base configuration class for Flask app."""

    # Flask core settings
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
    FLASK_DEBUG = os.getenv("FLASK_DEBUG", True)

    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql+psycopg2://car_user:car_pass@localhost:5432/car_report")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT configuration
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt-secret")

    # Celery configuration
    CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")
    CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND")

    # Back4App dataset API credentials
    BACK4APP_APP_ID = os.getenv("BACK4APP_APP_ID")
    BACK4APP_REST_KEY = os.getenv("BACK4APP_REST_KEY")
