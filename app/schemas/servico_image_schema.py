from marshmallow import Schema, fields, validate
from app.schemas.image_schema import  ImageSchema

class ServicoImageSchema(Schema):
    descricao = fields.Str(required=False,validate=validate.Length(0,200),allow_none=True)
    image = fields.Nested(ImageSchema, required=True, many=False, allow_none=False)
