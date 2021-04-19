from app import db
from .model import Model

class Usuario(db.Model,Model):
    id = db.Column(db.BigInteger,primary_key=True)
    nome = db.Column(db.String(100))
    email = db.Column(db.String(100))
    senha = db.Column(db.String(500))
    admin = db.Column(db.Boolean)
    img_path=db.Column(db.String(300))