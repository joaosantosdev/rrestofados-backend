from flask_mail import Message
import threading
from flask import render_template


def send_confirm_mail(email, code):
    from app import app, mail
    def func():
        message = Message('Confirmacao de email',
                          recipients=[email.lower().strip()],
                          sender=app.config['MAIL_USERNAME'])

        with app.app_context():
            message.html = render_template('email/confirmacao_email.html', code=code)
            mail.send(message)

    thread = threading.Thread(target=func)
    thread.start()
