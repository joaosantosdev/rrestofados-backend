from app import db
from .model import Model

class TipoServico(db.Model,Model):
    id = db.Column(db.BigInteger,primary_key=True)
    descricao = db.Column(db.String(100),nullable=False)