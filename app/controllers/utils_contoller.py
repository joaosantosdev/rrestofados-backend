from flask import Blueprint
from app.models.endereco import Estado,Municipio
from app.schemas.endereco_schema import EstadoSchema,MunicipioSchema
from app.security.token import security_token
from app.utils import const

utils_controller = Blueprint('utils',__name__)

@utils_controller.route('/estados',methods=['GET'])
@security_token()
def getEstados():
    estados = Estado.get_all()
    print(estados)
    return {
        'data':EstadoSchema(many=True).dump(estados)
    }


@utils_controller .route('/estado/<int:estadoId>/municipios',methods=['GET'])
@security_token()
def getMunicipios(estadoId):
    municipios = Municipio.filter_by(estado_id=estadoId)
    return {
        'data':MunicipioSchema(many=True).dump(municipios)
    }, const.http_status.get('OK')