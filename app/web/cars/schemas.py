# app/web/cars/car_schema.py

from marshmallow import fields, validate
from app import ma
from app.models.car import Car

class CarSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    make = fields.Str(required=True, validate=validate.Length(min=1))
    model = fields.Str(allow_none=True)
    year = fields.Int(allow_none=True)
    external_id = fields.Str(dump_only=True)
