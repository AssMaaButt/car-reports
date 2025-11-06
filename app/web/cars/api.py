# app/web/cars/cars_api.py

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.models.car import Car
from app.web.cars.schemas import CarSchema
from app import db

# Blueprint for car-related routes
cars_bp = Blueprint("cars", __name__, url_prefix="/cars")

car_schema = CarSchema()
cars_schema = CarSchema(many=True)

@cars_bp.route("/", methods=["GET"])
@jwt_required()
def list_cars():
    """List all cars with filters and pagination"""
    q = Car.query

    # Optional filters
    make = request.args.get("make")
    model = request.args.get("model")
    year = request.args.get("year", type=int)

    if make:
        q = q.filter(Car.make.ilike(f"%{make}%"))
    if model:
        q = q.filter(Car.model.ilike(f"%{model}%"))
    if year:
        q = q.filter_by(year=year)

    # Pagination
    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("per_page", default=20, type=int)
    paginated = q.order_by(Car.year.desc()).paginate(page=page, per_page=per_page, error_out=False)

    # Result structure
    result = {
        "total": paginated.total,
        "page": paginated.page,
        "per_page": paginated.per_page,
        "pages": paginated.pages,
        "items": cars_schema.dump(paginated.items),
    }
    return jsonify(result), 200
