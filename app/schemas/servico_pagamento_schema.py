from marshmallow import Schema, fields, ValidationError, pre_load
from app.models.forma_pagamento import FormaPagamento

class ServicoPagamentoSchema(Schema):
    id = fields.Int(required=False)
    valor = fields.Float(required=True, allow_none=False)
    formaPagamentoId = fields.Int(required=True, attribute='forma_pagamento_id')
    pago = fields.Boolean(required=True)

    @pre_load
    def valid_forma_pagamento(self, data, **kwargs):
        if data.get('formaPagamentoId'):
            formaPagamento = FormaPagamento.filter_one(id=data['formaPagamentoId'])
            
            if not formaPagamento:
                raise ValidationError('Forma de Pagamento inexistente')

        return data
