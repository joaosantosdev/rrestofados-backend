from app.models.servico_model import Servico
from app.models.servico_pagamento_model import ServicoPagamento
from app.models.cliente_model import Cliente
from app.models.cor import Cor
from app.models.tecido import Tecido
from app import db
from app.models.endereco import Endereco
from flask import request
import json
from app.models.pagination import Pagination
from sqlalchemy import any_,or_,and_

def get_paged():
    query = Servico.query.filter(Servico.status.in_([1, 2]))
    search = request.args.get('search', '{}', type=str)
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('perPage', 10, type=int)
    is_or = request.args.get('or', False, type=bool)

    search = json.loads(search)

    def compare(field, fieldName):
        return field == search.get(fieldName) if search.get(fieldName, None) is not None else True

    if is_or:
        query = query.filter(or_(compare(Cliente.nome, 'nome'),
                                 compare(Cliente.cpf, 'cpf'),
                                 compare(Cliente.email, 'email')))
    else:
        query = query.filter(compare(Cliente.nome, 'nome'))
        query = query.filter(compare(Cliente.email, 'email'))
        query = query.filter(compare(Cliente.cpf, 'cpf'))
        query = query.filter(compare(Tecido.id, 'tecido'))
        query = query.filter(compare(Cor.id, 'cor'))
    items = query.offset((page - 1) * per_page).limit(per_page).all()
    count = query.count()
    db.session.remove()
    pagination = Pagination(items, count, page)

    return pagination


def get_by_id(id):
    servico = Servico.filter_one(id=id)
    if servico:
        return servico, False
    return False, True


def save(data):

    try:
        print(data)

        servico = Servico()
        servico.update(data,['pagamentos', 'endereco'])
        servico.pagamentos = []

        for pagamento in data.get('pagamentos'):
            servico.pagamentos.append(ServicoPagamento(**pagamento))

        if data.get('endereco'):
            endereco = Endereco(**data['endereco'])
            db.session.add(endereco)
           

        db.session.add(servico)
        db.session.commit()
        id = servico.id
        db.session.remove()
        return id, False
    except Exception as e:
        print(e.__str__())
        return False, e.__str__()


def update(data, id):
    try:

        servico = Servico.filter_one(id=id)
        servico.update(data, ['pagamentos', 'endereco'])
        servico.pagamentos = []


        for pagamento in data.get('pagamentos'):
            servico.pagamentos.append(ServicoPagamento(**pagamento))

        if data.get('endereco'):
            endereco = servico.endereco if servico.endereco is not None else Endereco()
            endereco.update(data['endereco'])
            db.session.add(endereco)

        db.session.add(servico)
        db.session.commit()
        id = servico.id
        db.session.remove()
        return id, False
    except Exception as e:
        print(e.__str__())
        return False, e.__str__()