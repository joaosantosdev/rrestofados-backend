from flask import Blueprint
from app.services import tecido_service
from app.utils import const
from app.models.tecido import Tecido
from flask import request
from app.schemas.tecido_schema import TecidoSchema
from app import utils
from app.security.token import get_token,security_token,decode

tecido_view = Blueprint('tecido',__name__,url_prefix='/tecidos')
tecido_schema = TecidoSchema()

@tecido_view.route('',methods=['GET'])
@security_token
def get():
    pagination = Tecido.paginate_search()
    return utils.response_paged(schema=TecidoSchema, pagination=pagination)

@tecido_view.route('/all',methods=['GET'])
@security_token
def get_all():
    tecidos = Tecido.all()
    return utils.response_ok(TecidoSchema(many=True).dump(tecidos))



@tecido_view.route('/<int:id>',methods=['GET'])
@security_token
def get_by_id(id):
    tecido = Tecido.filter(id=id)
    if not tecido:
        return utils.response_not_found('Tecido não encontrado.')
    return tecido_schema.dump(tecido), const.http_status.get('OK')




@tecido_view.route('',methods=['POST'])
@security_token
def post():
    json = request.get_json()
    errors = tecido_schema.validate(json)
    if errors:
        return errors, const.http_status.get('BAD_REQUEST')
    auth = request.headers.get('Authorization')
    token = decode(auth)

    tecido = Tecido(**json)
    tecido.usuario_id = token.get('id')
    tecido,error = tecido_service.save(tecido)
    if error:
        return utils.response_server_error(error)

    return tecido_schema.dump(tecido), const.http_status.get('OK')


@tecido_view.route('/<int:id>',methods=['PUT'])
@security_token
def put(id):
    tecido = Tecido.filter(id=id)
    if not tecido:
        return utils.response_not_found('Tecido não encontrado.')

    json = request.get_json()
    errors = tecido_schema.validate(json)
    if errors:
        return errors, const.http_status.get('BAD_REQUEST')

    tecido.update(json,['id','usuario_id'])
    tecido,error = tecido_service.save(tecido)
    if error:
        return utils.response_server_error(error)
    return tecido_schema.dump(tecido), const.http_status.get('OK')