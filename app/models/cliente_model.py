from .model import Model
from app import db


class Cliente(Model, db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(15), nullable=True)
    cnpj = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    endereco_id = db.Column(db.BigInteger, db.ForeignKey('endereco.id'))
    endereco = db.relationship('Endereco', lazy='joined')
    telefones = db.relationship('Telefone', backref='cliente', lazy='joined')
    status = db.Column(db.Integer, nullable=False)
    fisica_juridica = db.Column(db.Integer, nullable=False)
