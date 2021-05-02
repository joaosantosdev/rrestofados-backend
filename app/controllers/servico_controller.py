from flask import Blueprint, request
from app.services import servico_service
from app.utils import response_paged, response_not_found, response_ok, response_bad_request, response_server_error
from app.schemas.servico_schema import ServicoSchema, ServicoCancelarSchema
from app.security.token import security_token
from app.schemas.servico_image_schema import ServicoImageSchema

servico_controller = Blueprint('ServicoController', __name__)
servico_schema = ServicoSchema()


@servico_controller.route('', methods=['GET'])
@security_token()
def get():
    paged = servico_service.get_paged()
    return response_paged(ServicoSchema, paged)


@servico_controller.route('/<int:id>', methods=['GET'])
@security_token()
def get_by_id(id):
    servico, error = servico_service.get_by_id(id)
    if error:
        return response_not_found('Serviço não encontrado.')

    return response_ok(servico_schema.dump(servico))


@servico_controller.route('', methods=['POST'])
@security_token()
def save():
    data = request.get_json()
    error = servico_schema.validate(data)
    if error:
        return response_bad_request(error)
    id, error = servico_service.save(servico_schema.load(data))
    if error:
        return response_server_error(error)
    return response_ok({
        'message': 'Serviço cadastrado com sucesso.',
        'id': id
    })


@servico_controller.route('/<int:id>', methods=['PUT'])
@security_token()
def update(id):
    data = request.get_json()

    error = servico_schema.validate(data)
    if error:
        return response_bad_request(error)

    id, error = servico_service.update(servico_schema.load(data), id)
    if error:
        return response_server_error(error)

    print(type(data))

    return response_ok('Serviço atualizado com sucesso.')


@servico_controller.route('/<int:id>/cancelar', methods=['PUT'])
@security_token()
def cancelar(id):
    data = request.get_json()

    error = ServicoCancelarSchema().validate(data)
    if error:
        return response_bad_request(error)

    id, error = servico_service.cancel(id, data.get('motivo'))
    if error:
        return response_server_error(error)

    return response_ok('Serviço cancelado com sucesso.')


@servico_controller.route('/<int:id>/images', methods=['POST'])
@security_token()
def save_images(id):
    data = request.get_json()

    error = ServicoImageSchema(many=True).validate(data)
    if error:
        return response_bad_request(error)

    servico = servico_service.get_by_id(id)
    if not servico:
        return response_server_error('Serviço não encontrado.')

    response, error = servico_service.save_images(id, data)
    if error:
        return response_server_error(error)
    return response_ok(response)


@servico_controller.route('/<int:id>/images', methods=['GET'])
@security_token()
def get_images(id):


    servico = servico_service.get_by_id(id)
    if not servico:
        return response_server_error('Serviço não encontrado.')


    response, error = servico_service.get_images(id)

    if error:
        return response_server_error(error)
    return response_ok(response)

