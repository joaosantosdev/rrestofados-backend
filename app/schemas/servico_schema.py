from marshmallow import Schema, fields, validate, pre_load, ValidationError
from app.schemas.endereco_schema import EnderecoSchema
from app.schemas.servico_pagamento_schema import ServicoPagamentoSchema
from marshmallow import post_load
from app.models.cliente_model import Cliente

class ClienteServicoSchema(Schema):
    id = fields.Int(required=False)
    nome = fields.Str(required=False)
    email = fields.Str(required=False)
    cpf = fields.Str(required=False)

class TecidoServicoSchema(Schema):
    descricao = fields.Str(required=False)

class CorServicoSchema(Schema):
    descricao = fields.Str(required=False)


class ServicoSchema(Schema):
    id = fields.Int(required=False)
    clienteId = fields.Int(required=True, attribute='cliente_id')
    cliente = fields.Nested(ClienteServicoSchema)
    tecido = fields.Nested(TecidoServicoSchema)
    cor = fields.Nested(CorServicoSchema)
    descricao = fields.Str(required=True, validate=validate.Length(1, 500))
    data = fields.Date(format='%Y-%m-%d', required=True)
    tecidoId = fields.Int(required=True, attribute='tecido_id')
    corId = fields.Int(required=True, attribute='cor_id')
    dataEntrega = fields.Date('%Y-%m-%d',required=False, attribute='data_entrega')
    endereco = fields.Nested(EnderecoSchema, required=False, allow_none=True)
    status = fields.Int(required=True)
    pagamentos = fields.List(fields.Nested(ServicoPagamentoSchema))
    valorFrete = fields.Float(required=False, allow_none=True, attribute='valor_frete')



    @pre_load
    def valid_cliente(self, data, **kwargs):
        if data.get('clienteId'):
            cliente = Cliente.filter_one(id=data['clienteId'])
            if not cliente:
                raise ValidationError('Cliente inexistente')
        return data
