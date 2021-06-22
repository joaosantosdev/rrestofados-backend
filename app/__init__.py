from flask import Flask
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import click
from flask.cli import with_appcontext
from flask_mail import Mail

import datetime

ma = Marshmallow()
db = SQLAlchemy()
migrate = Migrate(compare_type=True)


def create_app():
    app = Flask(__name__)
    if __name__ == 'app':
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ajfwdiszyqcoss:677d7778ab7dd4f99b7be74dd1f0d9caaf68683763b241c9105b4ee2ebf87e48@ec2-23-23-128-222.compute-1.amazonaws.com:5432/d166136c4a0gn5'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
        app.config['MAIL_PORT'] = 587
        app.config['MAIL_USE_TLS'] = True
        app.config['MAIL_USERNAME'] = 'suporte.rrestofados@gmail.com'
        app.config['MAIL_PASSWORD'] = 'Rr12345678'

        db.init_app(app)
        migrate.init_app(app, db)
        CORS(app)
        from app.controllers.usuario_controller import usuario_controller
        from app.controllers.cor_controller import cor_controller
        from app.controllers.tecido_controller import tecido_controller
        from app.controllers.forma_pagamento_controller import forma_pag_controller
        from app.controllers.utils_contoller import utils_controller
        from app.controllers.cliente_controller import cliente_controller
        from app.controllers.assets_controller import assets_controller
        from app.controllers.servico_controller import servico_controller
        from app.controllers.report_controller import report_controller
        from app.controllers.home_controller import home_controller
        from app.controllers.fluxo_caixa_controller import fluxo_caixa_controller

        app.register_blueprint(fluxo_caixa_controller, url_prefix='/fluxocaixa')
        app.register_blueprint(home_controller, url_prefix='/home')
        app.register_blueprint(report_controller, url_prefix='/reports')
        app.register_blueprint(servico_controller, url_prefix='/servicos')
        app.register_blueprint(assets_controller, url_prefix='/assets')
        app.register_blueprint(cliente_controller, url_prefix='/clientes')
        app.register_blueprint(utils_controller)
        app.register_blueprint(forma_pag_controller)
        app.register_blueprint(tecido_controller)
        app.register_blueprint(cor_controller)
        app.register_blueprint(usuario_controller, url_prefix='/usuario')

    return app


app = create_app()
mail = Mail(app)


@click.command(name='initdb')
@with_appcontext
def create_tables():
    with app.app_context():
        db.create_all()

app.cli.add_command(create_tables)