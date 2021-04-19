from functools import wraps
import jwt
from time import time
from app.models.usuario import Usuario
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

def valid_token(data):
    usuario = Usuario.query.filter_by(id=data['id']).first()
    if(data['expiration'] > int(time()*1000) and not usuario):
        return False
    return True

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
            if not valid_token(tokenDecoded):
                return error
        except:
            return error

        return func(*args, **kwargs)

    return wrapper

