# app/web/users/user_schemas.py

from marshmallow import fields, validate
from app import ma  # import the Marshmallow instance from your app
from app.models.user import User  # import the User model

class SignupSchema(ma.Schema):
    username = fields.Str(required=True, validate=validate.Length(min=3))
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True, validate=validate.Length(min=6))

class LoginSchema(ma.Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
