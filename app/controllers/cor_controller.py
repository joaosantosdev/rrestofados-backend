from flask import Blueprint
from app.services import cor_service
from app.utils import const
from app.models.cor import Cor
from flask import request
from app.schemas.cor_schema import CorSchema
from app import utils
from sqlalchemy import any_
from app.security.token import get_token,security_token,decode


cor_controller = Blueprint('cor',__name__,url_prefix='/cor')
cor_schema = CorSchema()

@cor_controller.route('',methods=['GET'])
@security_token()
def get():
    pagination = Cor.paginate_search()
    return utils.response_paged(schema=CorSchema, pagination=pagination)


@cor_controller.route('/all',methods=['GET'])
@security_token()
def get_all():
    cores = Cor.all()
    return utils.response_ok(CorSchema(many=True).dump(cores))    


@cor_controller.route('/<int:id>',methods=['GET'])
@security_token()
def get_by_id(id):
    cor = Cor.filter(id=id)
    if not cor:
        return utils.response_not_found('Cor não encontrada.')
    return cor_schema.dump(cor), const.http_status.get('OK')



@cor_controller.route('',methods=['POST'])
@security_token()
def post():
    json = request.get_json()
    errors = cor_schema.validate(json)
    if errors:
        return errors, const.http_status.get('BAD_REQUEST')

    cor = Cor(**json)
    cor,error = cor_service.save(cor)
    if error:
        return utils.response_server_error(error)

    return cor_schema.dump(cor), const.http_status.get('OK')


@cor_controller.route('/<int:id>',methods=['PUT'])
@security_token()
def put(id):
    cor = Cor.filter(id=id)
    if not cor:
        return utils.response_not_found('Cor não encontrada.')

    json = request.get_json()
    errors = cor_schema.validate(json)
    if errors:
        return errors, const.http_status.get('BAD_REQUEST')

    cor.update(json,['id'])
    cor,error = cor_service.save(cor)
    if error:
        return utils.response_server_error(error)
    return cor_schema.dump(cor), const.http_status.get('OK')
