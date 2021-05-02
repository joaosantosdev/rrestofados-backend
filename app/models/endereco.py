from app import db
from .model import Model

class Estado(db.Model,Model):
    id = db.Column(db.BigInteger,primary_key=True)
    sigla = db.Column(db.String(3),nullable=False)
    nome = db.Column(db.String(100),nullable=True)



class Municipio(db.Model,Model):
    id = db.Column(db.BigInteger,primary_key=True)
    estado_id = db.Column(db.BigInteger,db.ForeignKey('estado.id'))
    nome = db.Column(db.String(100),nullable=True)



class Endereco(db.Model,Model):
    id = db.Column(db.BigInteger,primary_key=True)
    estado_id = db.Column(db.BigInteger,db.ForeignKey('estado.id'))
    municipio_id = db.Column(db.BigInteger,db.ForeignKey('municipio.id'))
    cep = db.Column(db.String(50),nullable=True)
    bairro = db.Column(db.String(100),nullable=True)
    numero = db.Column(db.String(30),nullable=True)
    complemento = db.Column(db.String(30),nullable=True)
    rua = db.Column(db.String(100),nullable=True)
    estado = db.relationship('Estado', lazy='joined')
    municipio = db.relationship('Municipio', lazy='joined')

