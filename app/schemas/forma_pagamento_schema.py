from marshmallow import Schema,fields,validate

class FormaPagamentoSchema(Schema):
    id = fields.Int()
    nome = fields.Str(required=True,validate=validate.Length(0,100))
    descricao = fields.Str(required=True,allow_none=False,validate=validate.Length(0,100))
    usuario_id = fields.Str(required=False,allow_none=True)
    status = fields.Int(required=True,allow_none=False)


