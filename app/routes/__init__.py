# app/routes/__init__.py
# This file marks 'routes' as a Python package.
from .auth_routes import auth_bp
from .car_routes import car_bp
from flask import Blueprint, jsonify

main_bp = Blueprint("main", __name__)

@main_bp.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Flask app is running successfully!"}), 200

