from app import db
from app.models.cliente_model import Cliente
from app.models.endereco import Endereco
from app.models.telefone import Telefone
from app.schemas.endereco_schema import EnderecoSchema
from app.schemas.telefone_schema import TelefoneSchema
from app.schemas.cliente_schema import ClienteSchema
from app import utils
from app.utils import const
from sqlalchemy import or_, func
from flask import request
from app.models.pagination import  Pagination
import json

def saveListTelefone(telefones_data, cliente):
    for telefone_data in telefones_data:
        if telefone_data.get('clienteId'):
            del telefone_data['clienteId']

        if telefone_data.get('id'):
            del telefone_data['id']

        telefone = Telefone(**telefone_data)
        telefone.cliente_id = cliente.id
        db.session.add(telefone)
    db.session.commit()


def saveCliente(data):
    try:
        endereco_data = data.get('endereco')
        telefones_data = data.get('telefones')
        endereco = Endereco(**(EnderecoSchema().load(endereco_data)))
        db.session.add(endereco)

        del data['endereco']
        del data['telefones']

        cliente = Cliente(**data)
        cliente.endereco = endereco
        cliente.endereco_id = endereco.id
        db.session.add(cliente)
        db.session.commit()
        saveListTelefone(telefones_data, cliente)
        return True, False

    except Exception as e:
        print(e.__str__())
        return False, e.__str__()


def getAllPaginate():
    query = Cliente.query.filter(Cliente.status.in_([1, 2]))
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('perPage', 10, type=int)
    search = request.args.get('search', None, type=str)
    search = json.loads(search)

    def compareStr(field, fieldName):
        return func.lower(field) == search.get(fieldName, '').lower() if search.get(fieldName, None) is not None else True

    query = query.filter(or_(compareStr(Cliente.nome, 'nome'),
                             compareStr(Cliente.cpf, 'cpf'),
                             compareStr(Cliente.email, 'email')))

    items = query.offset((page - 1) * per_page).limit(per_page).all()
    count = query.count()
    db.session.remove()
    pagination = Pagination(items, count, page)

    return pagination


def getById(id):
    try:
        cliente = Cliente.filter_one(id=id)

        return cliente
    except Exception as e:
        return e.__str__()


def deleteCliente(cliente):
    try:
        cliente.status = const.status.get('DELETED')
        db.session.add(cliente)
        db.session.commit()
        db.session.remove()
        return cliente
    except Exception as e:
        return e.__str__()


def updateCliente(cliente, json):
    try:
        cliente.update(json, ['endereco', 'endereco_id', 'telefones'])

        cliente.endereco.update((EnderecoSchema().load(json.get('endereco'))), ['id'])
        print(cliente.endereco.rua)
        db.session.add(cliente.endereco)
        db.session.add(cliente)
        db.session.commit()
        Telefone.query.filter_by(cliente_id=cliente.id).delete()
        saveListTelefone(json.get('telefones'), cliente)

        return True, False
    except Exception as e:
        return False, e.__str__()
