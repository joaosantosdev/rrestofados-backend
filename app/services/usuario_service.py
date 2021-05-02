from app import db
from app.utils import save_image, delete_image
from app.models.image_model import Image
from app.models.code_verification_model import CodeVerification
from app import utils
import app.mail as mail


def save_image_usuario(usuario, data):
    if data.get('base64'):

        data.get('base64')
        name_img = 'usuario-$id'
        name_img = name_img.replace('$id', str(usuario.id))
        name = name_img + '.' + data.get('ext')
        save_image(name, 'usuarios', data.get('base64'))
        image = Image()
        if usuario.image_id:
            image = Image.get_one(id=usuario.image_id)
        image.name = name_img
        image.ext = data.get('ext')
        db.session.add(image)
        db.session.commit()
        return image


def delete_image_usuario(usuario):
    if usuario.image:
        delete_image(usuario.image.name + '.' + usuario.image.ext, 'usuarios')


def get_code_email(email, code):
    try:
        code = CodeVerification.query.filter_by(email=email, code=code).first()
        return code
    except Exception as e:
        return None


def save_code_verification(email, code):
    try:
        code_verification = CodeVerification()
        code_verification.code = code
        code_verification.email = email
        db.session.add(code_verification)
        db.session.commit()
        return code
    except Exception as e:
        return None


def remove_code_mail(email):
    try:
        code = CodeVerification.query.filter_by(email=email).delete()
        db.session.commit()
        return code
    except Exception as e:
        print(e.__str__())
        return None


def send_email_user(email, code):
    code_verification = get_code_email(email, code)
    if code and code_verification and code_verification.code == code:
        return False

    error = {'verification': 'Enviamos um Código de verificação para seu e-mail'}, 200
    if code and (not code_verification or code_verification.code != code):
        remove_code_mail(email)
        error = {'verification': 'Código inválido. Enviamos novamente um código de verificação para seu e-mail'}, 200

    code_generated = utils.generate_code()
    save_code_verification(email, code_generated)
    mail.send_confirm_mail(email, code_generated)
    db.session.remove()
    return error

def valid_email(usuario, email, code):
    code_verification = get_code_email(email, code)
    if email != usuario.email.lower().strip() and not code_verification:

        error = {'verification': 'Enviamos um Código de verificação para seu e-mail'}, 200
        if code and (not code_verification or code_verification.code != code):
            remove_code_mail(email)
            error = {
                        'verification': 'Código inválido. Enviamos novamente um código de verificação para seu e-mail'}, 200

        code_generated = utils.generate_code()
        save_code_verification(email, code_generated)
        mail.send_confirm_mail(email, code_generated)
        db.session.remove()
        return error

def update_image(usuario, image):
    if not image:
        delete_image_usuario(usuario)
        usuario.image_id = None
    else:
        image = save_image_usuario(usuario, image)
        if image:
            usuario.image_id = image.id
            usuario.image = image
    return usuario
