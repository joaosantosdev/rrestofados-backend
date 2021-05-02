from app import db
from .model import Model


class ServicoImage(db.Model, Model):
    id = db.Column(db.BigInteger, primary_key=True)
    descricao = db.Column(db.String(200), nullable=True)
    servico_id = db.Column(db.BigInteger, db.ForeignKey('servico.id'))
    image_id = db.Column(db.BigInteger, db.ForeignKey('image.id'))
    image = db.relationship('Image', lazy='joined')
