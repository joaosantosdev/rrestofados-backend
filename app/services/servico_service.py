from app.models.servico_model import Servico
from app.models.servico_pagamento_model import ServicoPagamento
from app.models.cliente_model import Cliente
from app import db
from app.models.endereco import Endereco
from flask import request
import json
from app.models.pagination import Pagination
from sqlalchemy import any_, or_, and_
from sqlalchemy import func
from app.models.image_model import Image
from app.models.servico_image_model import ServicoImage
from app.schemas.servico_image_schema import ServicoImageSchema
from app.utils import save_image, delete_image, get_image_base64


def get_paged():
    query = Servico.query.filter(Servico.status.in_([1, 2]))
    search = request.args.get('search', '{}', type=str)
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('perPage', 10, type=int)
    is_or = request.args.get('or', 'false', type=str) == 'true'

    search = json.loads(search)

    def compare(field, fieldName):
        return field == search.get(fieldName) if search.get(fieldName, None) is not None else True

    def compareStr(field, fieldName):
        return func.lower(field) == search.get(fieldName, '').lower() if search.get(fieldName,
                                                                                    None) is not None else True

    print()
    if is_or:
        query_cliente = Cliente.query.filter(Cliente.status.in_([1, 2]))

        query_cliente = query_cliente.filter(or_(compareStr(Cliente.nome, 'nome'),
                                                 compareStr(Cliente.cpf, 'cpf'),
                                                 compareStr(Cliente.email, 'email')))

        query = Servico.query.filter(Servico.cliente_id.in_(map(lambda cliente: cliente.id, query_cliente.all())))

    else:
        query = query.filter(and_(compare(Servico.status, 'status'),
                                  compare(Servico.tecido_id, 'tecido'),
                                  compare(Servico.cor_id, 'cor'),
                                  compare(Servico.cancelado, 'cancelado')))

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
        servico = Servico()
        servico.update(data, ['pagamentos', 'endereco'])
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
        return False, e.__str__()


def cancel(id, motivo):
    try:
        servico = Servico.filter_one(id=id)
        servico.motivo = motivo
        servico.cancelado = True
        db.session.add(servico)
        db.session.commit()
        db.session.remove()
        return True, False
    except Exception as e:
        return False, e.__str__()


def save_images(id_servico, lista):
    try:
        delete_servicos = ServicoImage.query.filter_by(servico_id=id_servico).all()
        for servico in delete_servicos:
            ServicoImage.query.filter_by(id=servico.id).delete()
            Image.query.filter_by(id=servico.image.id).delete()
            delete_image(servico.image.name + '.' + servico.image.ext, 'servicos')

        new_list = []
        i = 0
        for data in lista:
            name_img = 'servico-$id-image-$i'
            name_img = name_img.replace('$id', str(id_servico))
            name_img = name_img.replace('$i', str(i))
            name = name_img + '.' + data['image']['ext']

            if data['image'].get('base64'):
                save_image(name, 'servicos', data['image']['base64'])
                del data['image']['base64']

            image = Image(**data['image'])
            servico_image = ServicoImage(**data)

            servico_image.image = image
            servico_image.image.name = name_img
            servico_image.servico_id = id_servico
            new_list.append(servico_image)
            db.session.add(servico_image)
            i += 1
        db.session.commit()
        response = ServicoImageSchema(many=True).dump(new_list)
        db.session.remove()
        return response, False

    except Exception as e:
        return False, e.__str__()


def get_images(id_servico):
    try:
        lista = ServicoImage.query.filter_by(servico_id=id_servico)
        response = ServicoImageSchema(many=True).dump(lista)
        for data in response:
            data['image']['base64'] = get_image_base64(data['image']['name'], data['image']['ext'], 'servicos')
        db.session.remove()
        return response, False

    except Exception as e:
        return False, e.__str__()
