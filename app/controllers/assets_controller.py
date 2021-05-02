from flask import Blueprint, request, send_file
assets_controller = Blueprint('assets', __name__)


@assets_controller.route('/images',methods=['GET'])
def getImage():
    path = request.args.get('path')
    if not path:
        return '',404

    return send_file('assets/imgs/'+path, mimetype='image/png')


@assets_controller.route('/styles',methods=['GET'])
def get_styles():
    path = request.args.get('path')
    if not path:
        return '',404

    return send_file('assets/css/'+path, mimetype='text/css')


