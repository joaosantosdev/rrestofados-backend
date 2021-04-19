from marshmallow import Schema,fields,validate, pre_load, ValidationError
from app.models.endereco import Estado, Municipio 


class EnderecoSchema(Schema):
    id = fields.Int(required=False)
    estadoId = fields.Int(required=True,attribute='estado_id')
    municipioId = fields.Int(required=True,attribute='municipio_id')
    cep = fields.Str(required=False,allow_none=True)
    bairro = fields.Str(required=True,allow_none=True,validate=validate.Length(0,100))
    numero = fields.Str(required=True, allow_none=True,validate=validate.Length(0,30))
    complemento = fields.Str(required=False, allow_none=True,validate=validate.Length(0,30))
    rua = fields.Str(required=True, allow_none=True,validate=validate.Length(0,100))

    @pre_load
    def valid_estado(self, data, **kwargs):
        if data.get('estadoId'):
            estado = Estado.query.filter_by(id=data['estadoId']).first()
            if not estado:
                raise ValidationError('Estado inexistente')

        return data


    @pre_load
    def valid_municipio(self, data, **kwargs):
        if data.get('municipioId'):
            minicipio = Municipio.query.filter_by(id=data['municipioId']).first()
            if not minicipio:
                raise ValidationError('Municipio inexistente')

        return data


class EstadoSchema(Schema):
    id = fields.Int()
    sigla = fields.Str(required=True,validate=validate.Length(0,3))
    nome = fields.Str(required=False,allow_none=True,validate=validate.Length(0,100))


class MunicipioSchema(Schema):
    id = fields.Int()
    nome = fields.Str(required=False,allow_none=True,validate=validate.Length(0,100))




