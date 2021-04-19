from flask import Blueprint
from app.models.endereco import Estado,Municipio
from app.schemas.endereco_schema import EstadoSchema,MunicipioSchema
from app.security.token import security_token
from app.utils import const

utils_view = Blueprint('utils',__name__)

@utils_view.route('/estados',methods=['GET'])
def getEstados():
    estados = Estado.get_all()
    print(estados)
    return {
        'data':EstadoSchema(many=True).dump(estados)
    }


@utils_view.route('/estado/<int:estadoId>/municipios',methods=['GET'])
def getMunicipios(estadoId):
    municipios = Municipio.filter_by(estado_id=estadoId)
    return {
        'data':MunicipioSchema(many=True).dump(municipios)
    }, const.http_status.get('OK')