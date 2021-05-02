from marshmallow import Schema, fields, validate


class ImageSchema(Schema):
    id = fields.Int()
    name = fields.Str(required=False, validate=validate.Length(1, 100))
    ext = fields.Str(required=True, validate=validate.Length(1, 100))
    base64 = fields.Str(required=False)
