from app import db
from app.models.model import Model

class FluxoCaixa(db.Model,Model):
    id = db.Column(db.BigInteger,primary_key=True)
    data = db.Column(db.DateTime, nullable=False)
    descricao = db.Column(db.String(200),nullable=False)
    valor = db.Column(db.Float,nullable=False)


from app import db
from app.models.model import Model


