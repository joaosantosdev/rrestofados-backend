from flask import Blueprint, request, send_file, send_from_directory
from app.reports.servico_report import build_report_servico
from app.services import servico_service

from app.security.token import token_decode_valid
report_controller = Blueprint('report', __name__)

import os
@report_controller.route('/servico/<int:id>',methods=['GET'])
def servico_report_controller(id):
    token = request.args.get('token')
    usuario = token_decode_valid(token)
    print(os.path.abspath(__file__))
    if usuario:
        servico, error = servico_service.get_by_id(id)
        if error:
            return {'error': 'Servico não encontrado.'}

        name = build_report_servico(servico, usuario)

        return send_file(name, mimetype='application/pdf', as_attachment=True)
    return {}