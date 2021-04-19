from app import db
from .model import Model


class Tecido(db.Model,Model):
    id = db.Column(db.BigInteger,primary_key=True)
    nome = db.Column(db.String(100),nullable=False)
    descricao = db.Column(db.String(100),nullable=False)
    usuario_id = db.Column(db.BigInteger,db.ForeignKey('usuario.id'))
    status = db.Column(db.Integer,nullable=False)