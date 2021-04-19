from app.models.model import Model
from app import db


class ServicoPagamento(Model, db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    valor = db.Column(db.Float, nullable=False)
    forma_pagamento_id = db.Column(db.BigInteger, db.ForeignKey('forma_pagamento.id'))
    pago = db.Column(db.Boolean)
    servico_id = db.Column(db.BigInteger, db.ForeignKey('servico.id'))


    