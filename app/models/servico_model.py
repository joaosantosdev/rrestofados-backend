from app.models.model import Model
from app.models.tipo_servico_model import TipoServico
from app import db
class Servico(Model, db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    descricao = db.Column(db.String(500), nullable=False)
    observacao = db.Column(db.String(300), nullable=True)
    materiais_utilizados = db.Column(db.String(300), nullable=True)
    data = db.Column(db.DateTime, nullable=False)
    tecido_id = db.Column(db.BigInteger, db.ForeignKey('tecido.id'))
    tecido = db.relationship('Tecido', lazy='joined')
    cor_id = db.Column(db.BigInteger, db.ForeignKey('cor.id'))
    cor = db.relationship('Cor', lazy='joined')
    cliente = db.relationship('Cliente', lazy='joined')
    cliente_id = db.Column(db.BigInteger, db.ForeignKey('cliente.id'))
    data_entrega = db.Column(db.DateTime, nullable=True)
    endereco_id = db.Column(db.BigInteger, db.ForeignKey('endereco.id'))
    endereco = db.relationship('Endereco', lazy='joined')
    status = db.Column(db.Integer, nullable=False)
    valor_frete = db.Column(db.Float, nullable=True)
    pagamentos = db.relationship('ServicoPagamento', lazy='joined', backref='servico')
    cancelado = db.Column(db.Boolean, nullable=True, default=False)
    motivo = db.Column(db.String(200), nullable=True)
    tipo_servico_id = db.Column(db.BigInteger, db.ForeignKey('tipo_servico.id'), nullable=False)
