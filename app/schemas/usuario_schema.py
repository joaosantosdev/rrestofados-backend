from marshmallow import Schema,fields,validate
from app.schemas.image_schema import ImageSchema

class UsuarioAllSchema(Schema):
    id = fields.Int()
    nome = fields.Str(required=True, validate=validate.Length(1,100))
    email = fields.Email(required=True, validate=validate.Length(1,100))
    image = fields.Nested(ImageSchema, required=False, many=False, allow_none=True)
    status = fields.Int(required=True)

class UsuarioSchema(Schema):
    id = fields.Int()
    nome = fields.Str(required=True, validate=validate.Length(1,100))
    email = fields.Email(required=True, validate=validate.Length(1,100))
    senha = fields.Str(required=True, validate=validate.Length(0,500))
    admin = fields.Bool(required=True)
    image = fields.Nested(ImageSchema, required=False, many=False, allow_none=True)
    code = fields.Str(required=False)


class LoginSchema(Schema):
    email = fields.Email(required=True)
    senha = fields.Str(required=True)


class UserCreateSchema(Schema):
    nome = fields.Str(required=True, validate=validate.Length(1, 100))
    email = fields.Email(required=True, validate=validate.Length(1, 100))
    senha = fields.Str(required=True, validate=validate.Length(1, 500))
    code = fields.Str(required=False)

