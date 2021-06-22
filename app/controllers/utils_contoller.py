from flask import Blueprint
from app.models.endereco import Estado,Municipio
from app.schemas.endereco_schema import EstadoSchema,MunicipioSchema
from app.security.token import security_token
from app.utils import const
from app.models.tipo_servico_model import TipoServico
import app.utils as utils
from app.schemas.tipo_servico_schema import TipoServicoSchema

utils_controller = Blueprint('utils',__name__)

@utils_controller.route('/estados',methods=['GET'])
@security_token()
def getEstados():
    estados = Estado.get_all()
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




@utils_controller .route('/tiposservicos',methods=['GET'])
@security_token()
def get_tipo_servicos():
    tipos_servicos = TipoServico.get_all()
    return utils.response_ok(TipoServicoSchema(many=True).dump(tipos_servicos))