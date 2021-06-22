from flask import Blueprint, request
from app.schemas.params_graph_schema import ParamsGraphScham, ChartCancelados, ChartVendas, ChartRankingClientes, ChartTiposServicos
import app.utils as utils
from sqlalchemy import select, column
from app import db
import json
from app.security.token import security_token


home_controller = Blueprint('home', __name__)
schema = ParamsGraphScham()

@home_controller.route('/charts', methods=['POST'])
@security_token()
def home_data_chart():
    data = request.get_json()
    errors = schema.validate(data)

    if errors:
        return utils.response_bad_request(errors)

    params = json.dumps(data)
    result = db.engine.execute('SELECT * FROM f_view_chart_vendas(\':json\')'.replace(':json', params))
    vendas = ChartVendas(many=True).dump(list(result))

    result = db.engine.execute('SELECT * FROM f_view_chart_servicos_cancelados(\':json\')'.replace(':json', params))
    cancelados = ChartCancelados(many=True).dump(list(result))

    result = db.engine.execute('SELECT * FROM f_view_chart_ranking_clientes(\':json\')'.replace(':json', params))
    clientes = ChartRankingClientes(many=True).dump(list(result))

    result = db.engine.execute('SELECT * FROM f_view_chart_tipos_servicos(\':json\')'.replace(':json', params))
    tipos_servicos = ChartTiposServicos(many=True).dump(list(result))

    db.session.remove()
    return utils.response_ok({
        'vendas': vendas,
        'cancelados': cancelados,
        'clientes': clientes,
        'tiposServicos': tipos_servicos
    })