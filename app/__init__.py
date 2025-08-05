from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config
from app import models  # Esto carga todos los modelos


db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    # Importar y registrar Blueprints
    from app.controllers.gerencia_controller import gerencia_bp
    app.register_blueprint(gerencia_bp)


    return app