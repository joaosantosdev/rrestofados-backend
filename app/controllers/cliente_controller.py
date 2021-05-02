from flask import Blueprint, request
from app.schemas.cliente_schema import ClienteSchema
from app import utils
from app.services import cliente_service
from app.security.token import security_token

cliente_controller = Blueprint('cliente', __name__)
cliente_schema = ClienteSchema()

@cliente_controller.route('', methods=['POST'])
@security_token()
def post():
    json = request.get_json()
    error = cliente_schema.validate(json)
    if error:
        return utils.response_bad_request(error)

    print(error)

    success, error = cliente_service.saveCliente(json)
    if error:
        return utils.response_server_error(error)

    return utils.response_ok('Cliente cadastrado com sucesso.')


@cliente_controller.route('', methods=['GET'])
@security_token()
def get():
    pagination = cliente_service.getAllPaginate()
    return utils.response_paged(ClienteSchema, pagination)

@cliente_controller.route('/<int:id>', methods=['GET'])
@security_token()
def getById(id):
    cliente = cliente_service.getById(id)
    if not cliente:
        return utils.response_not_found('Cliente não encontrado.')

    return utils.response_ok(cliente_schema.dump(cliente))

@cliente_controller.route('/<int:id>', methods=['DELETE'])
@security_token()
def deleteById(id):
    cliente = cliente_service.getById(id)
    if not cliente:
        return utils.response_not_found('Cliente não encontrado.')

    deleted = cliente_service.deleteCliente(cliente)

    if deleted:
        return utils.response_ok('Cliente removido com sucesso.')

    return utils.response_server_error(deleted)


@cliente_controller.route('/<int:id>', methods=['PUT'])
@security_token()
def updateCliente(id):
    json = request.get_json()
    error = cliente_schema.validate(json)
    if error:
        return utils.response_bad_request(error)

    cliente = cliente_service.getById(id)
    if not cliente:
        return utils.response_not_found('Cliente não encontrado.')

    success, error = cliente_service.updateCliente(cliente,json)
    if success:
        return utils.response_ok('Cliente atualizado com sucesso.')
    return utils.response_ok(error)

