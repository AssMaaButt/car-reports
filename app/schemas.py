# app/schemas.py
from . import ma
from marshmallow import fields, validate, validates, ValidationError
from .models.models import User, Car

class SignupSchema(ma.Schema):
    username = fields.Str(required=True, validate=validate.Length(min=3))
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True, validate=validate.Length(min=6))

class LoginSchema(ma.Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)

class CarSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    make = fields.Str(required=True, validate=validate.Length(min=1))
    model = fields.Str(allow_none=True)
    year = fields.Int(allow_none=True)
    external_id = fields.Str(dump_only=True)
