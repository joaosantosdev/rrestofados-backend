from flask import Flask
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

ma = Marshmallow()
db = SQLAlchemy()
migrate = Migrate(compare_type=True)


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:061118@localhost:5432/rrestofados'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)
    from app.controllers.usuario_view import usuarioView
    from app.controllers.cor_view import cor_view
    from app.controllers.tecido_view import tecido_view
    from app.controllers.forma_pagamento_view import forma_pag_view
    from app.controllers.utils_view import utils_view
    from app.controllers.cliente_controller import cliente_controller
    from app.controllers.assets_controller import assets_controller
    from app.controllers.servico_controller import servico_controller

    app.register_blueprint(servico_controller, url_prefix='/servicos')
    app.register_blueprint(assets_controller, url_prefix='/assets')
    app.register_blueprint(cliente_controller, url_prefix='/clientes')
    app.register_blueprint(utils_view)
    app.register_blueprint(forma_pag_view)
    app.register_blueprint(tecido_view)
    app.register_blueprint(cor_view)
    app.register_blueprint(usuarioView)

    return app


if __name__ == '__main__':
    app = create_app()

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()

    print(app.url_map)

    app.run(debug=True, host='0.0.0.0', threaded=True)
