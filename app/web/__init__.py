# app/web/__init__.py
# This file marks 'web' as a Python package and registers blueprints.

from flask import Blueprint, jsonify
from app.web.users.api import users_bp
from app.web.cars.api import cars_bp

# Optional main blueprint for the root endpoint
main_bp = Blueprint("main", __name__)

@main_bp.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Flask app is running successfully!"}), 200