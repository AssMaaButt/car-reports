from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class Car(db.Model):
    __tablename__ = "cars"
    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(120), nullable=False, index=True)
    model = db.Column(db.String(120), nullable=True, index=True)
    year = db.Column(db.Integer, nullable=True, index=True)
    external_id = db.Column(db.String(128), unique=True, nullable=True, index=True)  # Back4App objectId
    created_at = db.Column(db.DateTime, nullable=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "make": self.make,
            "model": self.model,
            "year": self.year,
            "external_id": self.external_id,
        }
