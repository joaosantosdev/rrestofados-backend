from app import db
from .model import Model


class Usuario(db.Model, Model):
    id = db.Column(db.BigInteger, primary_key=True)
    nome = db.Column(db.String(100))
    email = db.Column(db.String(100))
    senha = db.Column(db.String(500))
    admin = db.Column(db.Boolean)
    image_id = db.Column(db.BigInteger, db.ForeignKey('image.id'), nullable=True)
    image = db.relationship('Image', lazy=True)
    created_by = db.Column(db.BigInteger, db.ForeignKey('usuario.id'), nullable=True)
    date_created = db.Column(db.DateTime, nullable=False)
    date_updated = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.Integer, nullable=False)
