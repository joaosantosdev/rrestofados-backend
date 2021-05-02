from functools import wraps
import jwt
from time import time
from app.models.usuario_model import Usuario
SECRET_KEY = "123"

def get_token(data):
    data['expiration'] = int(time()*1000) + 86400000
    print(data)
    return enconde(data).decode('UTF-8')

def enconde(data):
    encoded = jwt.encode(data, SECRET_KEY, algorithm='HS256')
    return encoded

def decode(enconde):
    decode = jwt.decode(enconde, SECRET_KEY, algorithm='HS256')
    return decode

def valid_token(data, only_admin = False):
    usuario = Usuario.query.filter_by(id=data['id']).first()
    if(data['expiration'] > int(time()*1000) and not usuario) or (only_admin and not usuario.admin):
        return False
    return usuario


def token_decode_valid(token):
    if not token:
        return False
    try:
        tokenDecoded = decode(token)
        usuario = valid_token(tokenDecoded)
        if not usuario:
            return False
        return usuario
    except:
        return False

def security_token(only_admin=False):
    def security_token(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            from flask import request
            token = request.headers.get('Authorization')

            if not token:
                return {'message':'header sem token'},401
            error = {'message': 'Token invalido'}, 401
            try:
                tokenDecoded = decode(token)
                if not valid_token(tokenDecoded, only_admin):
                    return error
            except:
                return error

            return func(*args, **kwargs)

        return wrapper
    return security_token

