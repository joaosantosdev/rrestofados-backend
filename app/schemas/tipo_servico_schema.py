from marshmallow import Schema,fields,validate

class TipoServicoSchema(Schema):
    id = fields.Int()
    descricao = fields.Str(validate=validate.Length(0,100))


