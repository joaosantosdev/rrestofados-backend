from marshmallow import Schema,fields

class UsuarioSchema(Schema):
    id = fields.Int()
    nome = fields.Str(required=True)
    email = fields.Email(required=True)
    senha = fields.Str(required=True)
    fotoPath = fields.Str(allow_none=True, attribute='img_path')
    fotoBase64 = fields.Str(allow_none=True)
    fotoExt = fields.Str(allow_none=True)

    admin = fields.Bool(required=True)

class LoginSchema(Schema):
    email = fields.Email(required=True)
    senha = fields.Str(required=True)

