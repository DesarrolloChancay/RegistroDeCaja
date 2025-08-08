from flask import Flask
from app.config import Config
from app.extensions import db  # <- import desde extensions

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    # Importar y registrar Blueprints
    from app.controllers.gerencia_controller import gerencia_bp
    app.register_blueprint(gerencia_bp)

    return app