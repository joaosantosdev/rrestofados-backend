from .model import Model
from app import db

class Telefone(Model,db.Model):
    id = db.Column(db.BigInteger,primary_key=True)
    numero = db.Column(db.String(20),nullable=False)
    descricao = db.Column(db.String(100),nullable=False)
    whatsapp = db.Column(db.Boolean(),nullable=False)
    cliente_id = db.Column(db.BigInteger,db.ForeignKey('cliente.id'))
