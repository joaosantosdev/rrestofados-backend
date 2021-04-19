from app.schemas.usuario_schema import UsuarioSchema, LoginSchema
from app.security.token import get_token, security_token, decode
from flask_cors import cross_origin
from app.models.usuario import Usuario
from flask import request
from flask import Blueprint
from app import db
import base64
from app.utils import saveImage, getImage, deleteImage
import bcrypt

loginSchema = LoginSchema()
usuarioSchema = UsuarioSchema()
usuarioView = Blueprint('usuario', __name__, url_prefix='/usuario')


@usuarioView.route('/logado', methods=['GET'])
@security_token
def get_usuario_logado():
    auth = request.headers.get('Authorization')
    token = decode(auth)
    usuario = Usuario.query.filter_by(id=token['id']).first()
    if usuario.img_path:
        usuario.fotoBase64 = getImage(usuario.img_path, 'usuarios')
    data = usuarioSchema.dump(usuario)
    del data['senha']
    return data, 200


@usuarioView.route('', methods=['POST'])
def create_user():
    json = request.get_json()
    errors = usuarioSchema.validate(json)
    if errors:
        return errors, 500

    data = usuarioSchema.loads(request.get_data())
    usuarioEmail = Usuario.query.filter_by(email=data['email']).first()
    if (usuarioEmail):
        return {'message': 'Email ja possui cadastro.'}, 500
    data['senha'] = bcrypt.hashpw(str.encode(data.get('senha')), bcrypt.gensalt()).decode()
    usuario = Usuario(**data)
    db.session.add(usuario)
    db.session.commit()
    response = usuarioSchema.dump(usuario)
    del response['senha']
    return response, 200


@usuarioView.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    errors = loginSchema.validate(data)
    if errors:
        return errors, 500
    usuarioEmail = Usuario.query.filter_by(email=data['email']).first()
    if not usuarioEmail:
        return {'message': 'Usuario nao encontrado.'}, 404


    if not bcrypt.checkpw(str.encode(data.get('senha')), str.encode(usuarioEmail.senha)):
        return {'message': 'Senha incorreta'}, 500
    data = usuarioSchema.dump(usuarioEmail)
    del data['senha']
    token = get_token({'id': usuarioEmail.id})
    return {'token': token, 'usuario': data}, 200


@usuarioView.route('/<int:id>', methods=['PUT'])
@security_token
def update_usuario(id):
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
    usuario = Usuario.query.filter_by(id=id).first()

    if json['fotoBase64']:
        nameImage = 'usuario-$id.$ext'
        nameImage = nameImage.replace('$id', str(usuario.id))
        nameImage = nameImage.replace('$ext', json['fotoExt'])
        img_path = saveImage(nameImage,'usuarios', json['fotoBase64'])
        print(img_path)
        if img_path:
            usuario.img_path = img_path
    elif usuario.img_path:
        deleteImage(usuario.img_path,'usuarios')
        usuario.img_path = None

    del json['admin']
    usuario.update(json, not_update=['id'])
    db.session.commit()
    response = usuarioSchema.dump(usuario)
    del response['senha']
    return response, 200
