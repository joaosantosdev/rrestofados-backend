from flask import Blueprint, request
from app.services import servico_service
from app.utils import response_paged, response_not_found, response_ok, response_bad_request, response_server_error
from app.schemas.servico_schema import ServicoSchema

servico_controller = Blueprint('ServicoController', __name__)
servico_schema = ServicoSchema()


@servico_controller.route('', methods=['GET'])
def get():
    paged = servico_service.get_paged()
    return response_paged(ServicoSchema, paged)


@servico_controller.route('/<int:id>', methods=['GET'])
def get_by_id(id):
    servico, error = servico_service.get_by_id(id)
    if error:
        return response_not_found('Serviço não encontrado.')

    return response_ok(servico_schema.dump(servico))


@servico_controller.route('', methods=['POST'])
def save():
    data = request.get_json()
    error = servico_schema.validate(data)
    if error:
        return response_bad_request(error)
    id, error = servico_service.save(servico_schema.load(data))
    if error:
        return response_server_error(error)
    return response_ok({
        'message':'Serviço cadastrado com sucesso.',
        'id': id
    })


@servico_controller.route('/<int:id>', methods=['PUT'])
def update(id):
    data = request.get_json()

    error = servico_schema.validate(data)
    if error:
        return response_bad_request(error)

    id, error = servico_service.update(servico_schema.load(data), id)
    if error:
        return response_server_error(error)

    return response_ok('Serviço atualizado com sucesso.')