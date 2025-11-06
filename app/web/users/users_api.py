# app/web/users/users_api.py

from flask import Blueprint, request, jsonify
from app import db
from app.models.user import User
from app.web.users.user_schemas import SignupSchema, LoginSchema
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash

# Blueprint for user-related routes
users_bp = Blueprint("users", __name__, url_prefix="/auth")

signup_schema = SignupSchema()
login_schema = LoginSchema()

@users_bp.route("/signup", methods=["POST"])
def signup():
    """Handle user registration"""
    payload = request.get_json() or {}
    errors = signup_schema.validate(payload)
    if errors:
        return jsonify({"errors": errors}), 400

    username = payload["username"]
    email = payload["email"]
    password = payload["password"]

    # prevent duplicate users
    if User.query.filter((User.username == username) | (User.email == email)).first():
        return jsonify({"error": "username or email already exists"}), 409

    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify({
        "message": "User created successfully",
        "user": {"id": user.id, "username": user.username}
    }), 201


@users_bp.route("/login", methods=["POST"])
def login():
    """Handle user login"""
    payload = request.get_json() or {}
    errors = login_schema.validate(payload)
    if errors:
        return jsonify({"errors": errors}), 400

    username = payload["username"]
    password = payload["password"]

    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(identity=str(user.id))
    return jsonify({"access_token": access_token}), 200
