import base64
import os
from app.utils import const

from flask import make_response

def saveImage(name,subpath,fotobase64):
    try:
        file_path = '../assets/imgs/$subpath/$name'
        file_path = file_path.replace('$subpath',subpath)
        file_path = file_path.replace("$name", name)
        imgdata = base64.b64decode(fotobase64)
        with open(file_path, 'wb') as f:
            f.write(imgdata)
        return name
    except Exception as e:

        return False

def getImage(name,subpath):
    print(name)
    file_path = '../assets/imgs/$subpath/$name'
    file_path = file_path.replace('$subpath', subpath)
    file_path = file_path.replace("$name", name)
    print(file_path)
    with open(file_path, "rb") as image_file:
        ext = name.split('.')[1]
        response = "data:image/$ext;base64,"
        response = response.replace('$ext',ext)
        print(ext)
        return response+base64.b64encode(image_file.read()).decode('ascii')

def deleteImage(name,subpath):
    file_path = '../assets/imgs/$subpath/$name'
    file_path = '../assets/imgs/$subpath/$name'
    file_path = file_path.replace('$subpath', subpath)
    file_path = file_path.replace("$name", name)
    os.remove(file_path)



def response_bad_request(error):
    return make_response({'error':error},const.http_status.get('BAD_REQUEST'))

def response_server_error(error):
    return make_response({
        'error':error
    },const.http_status.get('SERVER_ERROR'))

def response_created(data):
    return make_response({
        'data':data
    },const.http_status.get('CREATED'))

def response_ok(data):
    return make_response({
        'data':data
    },const.http_status.get('OK'))

def response_paged(schema,pagination):
    items = schema(many=True).dump(pagination.items)
    return {
        'data': items,
        'totalCount': pagination.total,
        'page': pagination.page,
        'count': len(items)
    }, const.http_status.get('OK')


def response_not_found(message):
    return {'error':message}, const.http_status.get('NOT_FOUND')

def response_server_error(message):
    return {'error':message}, const.http_status.get('SERVER_ERROR')
