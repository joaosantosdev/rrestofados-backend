from flask import Blueprint, request, send_file
assets_controller = Blueprint('assets', __name__)


@assets_controller.route('/images',methods=['GET'])
def getImage():
    path = request.args.get('path')
    if not path:
        return '',404

    return send_file('../assets/imgs/'+path, mimetype='image/png')