from app.schemas.usuario_schema import UsuarioSchema, LoginSchema, UserCreateSchema,UsuarioAllSchema
from app.security.token import get_token, security_token, decode
from app.models.usuario_model import Usuario
from flask import request
from flask import Blueprint
from app import db
from app import utils
from app.utils import const

import bcrypt
from app.services import usuario_service
from flask import session
from datetime import datetime

loginSchema = LoginSchema()
usuarioSchema = UsuarioSchema()
usuario_controller= Blueprint('usuario', __name__, url_prefix='/usuario')


@usuario_controller.route('/logado', methods=['GET'])
@security_token()
def get_usuario_logado():
    auth = request.headers.get('Authorization')
    token = decode(auth)
    usuario = Usuario.query.filter_by(id=token['id']).first()
    data = usuarioSchema.dump(usuario)
    del data['senha']
    return data, 200

@usuario_controller.route('', methods=['GET'])
@security_token(only_admin=True)
def get_users():
    auth = request.headers.get('Authorization')
    token = decode(auth)
    usuario = Usuario.query.filter(Usuario.created_by==token['id']).order_by(Usuario.nome.desc()).all()

    list = UsuarioAllSchema(many=True).dump(usuario)

    return utils.response_ok(list)

@usuario_controller.route('/<int:id>/updatestatus', methods=['GET'])
@security_token(only_admin=True)
def update_status(id):
    usuario = Usuario.query.filter_by(id=id,admin=False).first()
    if not usuario:
        return utils.response_bad_request('Usuário não encontrado.')

    usuario.status = const.status.get('ativo') if usuario.status == const.status.get('inativo') else const.status.get('inativo')

    db.session.commit()
    db.session.remove()

    return utils.response_ok('Status atualizado com sucesso.')

@usuario_controller.route('', methods=['POST'])
@security_token(only_admin=True)
def create_user():
    json = request.get_json()
    schema = UserCreateSchema()
    errors = schema.validate(json)
    if errors:
        return errors, 500
    data = schema.loads(request.get_data())
    email = data['email'].lower().strip()
    usuarioEmail = Usuario.query.filter_by(email=email).first()
    if (usuarioEmail):
        return utils.response_bad_request('Email já possui cadastro.')
    code = data.get('code')
    invalid_email = usuario_service.send_email_user(email, code)
    if invalid_email:
        return invalid_email

    data['email'] = email
    data['senha'] = bcrypt.hashpw(str.encode(data.get('senha')), bcrypt.gensalt()).decode()
    data['status'] = const.status.get('ativo')
    data['admin'] = False
    del data['code']
    auth = request.headers.get('Authorization')
    token = decode(auth)
    usuario = Usuario(**data)
    usuario.created_by = token['id']
    usuario.date_created = datetime.now()
    db.session.add(usuario)
    db.session.commit()
    response = usuarioSchema.dump(usuario)
    db.session.remove()
    del response['senha']
    return utils.response_created('Usuário cadastrado com sucesso.')


@usuario_controller.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    errors = loginSchema.validate(data)
    if errors:
        return errors, 500
    usuarioEmail = Usuario.query.filter_by(email=data['email'], status=const.status.get('ativo')).first()
    if not usuarioEmail:
        return {'message': 'Usuario não encontrado.'}, 404

    if not bcrypt.checkpw(str.encode(data.get('senha')), str.encode(usuarioEmail.senha)):
        return {'message': 'Senha incorreta'}, 500
    data = usuarioSchema.dump(usuarioEmail)
    del data['senha']
    token = get_token({'id': usuarioEmail.id})
    return {'token': token, 'usuario': data}, 200



@usuario_controller.route('', methods=['PUT'])
@security_token()
def update_usuario():
    json = request.get_json()
    is_senha = json.get('senha')
    if not is_senha:
        json['senha'] = ''
    json['admin'] = False


    errors = usuarioSchema.validate(json)
    if errors:
        return errors, 400

    if not is_senha:
        del json['senha']

    auth = request.headers.get('Authorization')
    token = decode(auth)
    usuario = Usuario.query.filter_by(id=token['id']).first()
    email = json.get('email').lower().strip()
    code = json.get('code')

    if email != usuario.email and  Usuario.query.filter_by(email=email).first():
        return utils.response_bad_request('Email já possui cadastro.')


    invalid_email = usuario_service.valid_email(usuario, email, code)
    if invalid_email:
        return invalid_email

    usuario_service.remove_code_mail(email)
    usuario_service.remove_code_mail(usuario.email)

    image = json.get('image')

    del json['admin']
    usuario.update(json, not_update=['id', 'image'])
    usuario = usuario_service.update_image(usuario, image)
    usuario.date_updated = datetime.now()
    db.session.commit()
    response = usuarioSchema.dump(usuario)
    del response['senha']
    return response, 200
