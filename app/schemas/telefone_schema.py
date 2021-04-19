from marshmallow import Schema,fields,validate

class TelefoneSchema(Schema):
    numero = fields.String(required=True,validate=validate.Length(1,20))
    descricao = fields.String(required=True,validate=validate.Length(1,100))
    whatsapp = fields.Boolean(required=True,allow_none=False)
    clienteId = fields.Int(required=False,allow_none=True,attribute='cliente_id')
