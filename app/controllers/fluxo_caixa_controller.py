from flask import Blueprint, request
from app.schemas.fluxo_caixa_schema import FluxoCaixaSchema,FluxoCaixaFiltersSchema
import app.utils as utils
from app.models.fluxo_caixa_model import FluxoCaixa

from sqlalchemy import select, column
from app import db
import json
from app.security.token import security_token


fluxo_caixa_controller = Blueprint('fluxo_caixa', __name__)
schema = FluxoCaixaSchema()
schema_filters = FluxoCaixaFiltersSchema()

@fluxo_caixa_controller.route('', methods=['POST'])
@security_token()
def post():
    data = request.get_json()
    print(data)
    errors = schema.validate(data)

    if errors:
        return utils.response_bad_request(errors)

    fluxo_caixa = FluxoCaixa(**schema.load(data))
    try:
        db.session.add(fluxo_caixa)
        db.session.commit()
        db.session.remove()
        return utils.response_created('Registro salvo com sucesso.')
    except Exception as e:
        return utils.response_server_error(e.__str__())



@fluxo_caixa_controller.route('/filters', methods=['POST'])
@security_token()
def get_by_filters():
    data = request.get_json()
    errors = schema_filters.validate(data)

    if errors:
        return utils.response_bad_request(errors)

    result = db.engine.execute('SELECT * FROM f_view_fluxo_caixa(\':json\')'.replace(':json', json.dumps(data)))
    return utils.response_ok(FluxoCaixaSchema(many=True).dump(list(result)))



@fluxo_caixa_controller.route('/<int:id>', methods=['DELETE'])
@security_token()
def delete(id):
    try:
        FluxoCaixa.query.filter_by(id=id).delete()
        db.session.commit()
        db.session.remove()
        return utils.response_ok('Registro removido com sucesso.')
    except Exception as e:
        return utils.response_not_found('Registro não encontrado.')
