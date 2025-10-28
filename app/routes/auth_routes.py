# app/routes/auth_routes.py
from flask import Blueprint, request, jsonify
from .. import db
from ..models import User
from ..schemas import SignupSchema, LoginSchema
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

signup_schema = SignupSchema()
login_schema = LoginSchema()

@auth_bp.route("/signup", methods=["POST"])
def signup():
    payload = request.get_json() or {}
    errors = signup_schema.validate(payload)
    if errors:
        return jsonify({"errors": errors}), 400

    username = payload["username"]
    email = payload["email"]
    password = payload["password"]

    # prevent duplicates
    if User.query.filter((User.username == username) | (User.email == email)).first():
        return jsonify({"error": "username or email already exists"}), 409

    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "user created", "user": {"id": user.id, "username": user.username}}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    payload = request.get_json() or {}
    errors = login_schema.validate(payload)
    if errors:
        return jsonify({"errors": errors}), 400

    username = payload["username"]
    password = payload["password"]

    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({"error": "invalid credentials"}), 401

    access_token = create_access_token(identity=str(user.id))
    return jsonify({"access_token": access_token}), 200
