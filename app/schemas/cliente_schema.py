from marshmallow import Schema,fields,validate
from app import db
from .endereco_schema import EnderecoSchema
from .telefone_schema import TelefoneSchema

class ClienteSchema(Schema):
    id = fields.Int()
    nome = fields.Str(required=True,validate=validate.Length(0,100))
    cpf = fields.Str(required=False,validate=validate.Length(0,15),allow_none=True)
    email = fields.Str(required=False, allow_none=True)
    status = fields.Int(required=True,allow_none=False)
    endereco = fields.Nested(EnderecoSchema,required=True,allow_none=False)
    telefones = fields.Nested(TelefoneSchema,required=True,allow_none=False,many=True)
    fisicaJuridica = fields.Int(required=True,allow_none=False, attribute='fisica_juridica')
    cnpj = fields.Str(required=False,validate=validate.Length(0,20),allow_none=True)
