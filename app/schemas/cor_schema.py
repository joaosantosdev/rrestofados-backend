from marshmallow import Schema,fields,validate
class CorSchema(Schema):
    id = fields.Int()
    nome = fields.Str(required=True,validate=validate.Length(0,100))
    descricao = fields.Str(required=False,allow_none=True,validate=validate.Length(0,100))
    hexadecimal = fields.Str(required=False,allow_none=True,validate=validate.Length(0,100))
    status = fields.Int(required=True,allow_none=False)


