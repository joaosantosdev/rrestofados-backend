from marshmallow import Schema, fields, validate


class FluxoCaixaSchema(Schema):
    id = fields.Int(required=False, allow_none=True)
    tipo = fields.Int(required=False, allow_none=True)
    data = fields.DateTime(required=True)
    valor = fields.Float(required=False, allow_none=False)
    descricao = fields.Str(required=True, validate=validate.Length(1, 200))

class FluxoCaixaFiltersSchema(Schema):
    dataInicial = fields.Date(required=True)
    dataFinal = fields.Date(required=True)

