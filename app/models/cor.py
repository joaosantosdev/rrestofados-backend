from app import db
from .model import Model

class Cor(db.Model,Model):
    id = db.Column(db.BigInteger,primary_key=True)
    nome = db.Column(db.String(100),nullable=False)
    descricao = db.Column(db.String(100),nullable=True)
    hexadecimal = db.Column(db.String(15),nullable=True)
    status = db.Column(db.Integer,nullable=False)