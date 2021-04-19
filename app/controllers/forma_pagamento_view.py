from flask import Blueprint
from app.utils import const
from app.models.forma_pagamento import FormaPagamento
from app.services import forma_pagamento_service
from flask import request
from app.schemas.forma_pagamento_schema import FormaPagamentoSchema
from app import utils
from app.security.token import  security_token, decode

forma_pag_view = Blueprint('formaPagamento', __name__, url_prefix='/formapagamento')
forma_pag_schema = FormaPagamentoSchema()


@forma_pag_view.route('', methods=['GET'])
@security_token
def get():
    pagination = FormaPagamento.paginate_search()
    return utils.response_paged(schema=FormaPagamentoSchema, pagination=pagination)


@forma_pag_view.route('/all', methods=['GET'])
@security_token
def get_all():
    formasPagamentos = FormaPagamento.all()
    return utils.response_ok(FormaPagamentoSchema(many=True).dump(formasPagamentos))



@forma_pag_view.route('/<int:id>', methods=['GET'])
@security_token
def get_by_id(id):
    forma = FormaPagamento.filter(id=id)
    if not forma:
        return utils.response_not_found('Forma de pagamento não encontrada.')
    return forma_pag_schema.dump(forma), const.http_status.get('OK')


@forma_pag_view.route('', methods=['POST'])
@security_token
def post():
    json = request.get_json()
    errors = forma_pag_schema.validate(json)
    if errors:
        return errors, const.http_status.get('BAD_REQUEST')
    auth = request.headers.get('Authorization')
    token = decode(auth)

    forma = FormaPagamento(**json)
    forma.usuario_id = token.get('id')
    forma, error = forma_pagamento_service.save(forma)
    if error:
        return utils.response_server_error(error)

    return forma_pag_schema.dump(forma), const.http_status.get('OK')


@forma_pag_view.route('/<int:id>', methods=['PUT'])
@security_token
def put(id):
    forma = FormaPagamento.filter(id=id)
    if not forma:
        return utils.response_not_found('Tecido não encontrado.')

    json = request.get_json()
    errors = forma_pag_schema.validate(json)
    if errors:
        return errors, const.http_status.get('BAD_REQUEST')

    forma.update(json, ['id', 'usuario_id'])
    forma, error = forma_pagamento_service.save(forma)
    if error:
        return utils.response_server_error(error)
    return forma_pag_schema.dump(forma), const.http_status.get('OK')
