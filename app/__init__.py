from flask import Flask, render_template, request, redirect, url_for, flash
from app.config import Config
from app.extensions import db, login_manager
from flask_login import login_user, logout_user, login_required, current_user
from flask import Blueprint
from app.models.Usuario import Usuario
from app.controllers.gerencia_controller import *
from flask import session
from flask import make_response

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form['email']
        contrasena = request.form['password']
        user = Usuario.query.filter_by(
            correo=correo, contrasena=contrasena).first()
        if user:
            login_user(user)
            session['rol'] = user.rol.nombre
            session['name'] = user.nombre
            session['titulo'] = create_titulo(session['rol'])
            return redirect(url_for('gerencia_bp.auditoria'))
        else:
            flash('Usuario o contraseña incorrectos', 'danger')
    return render_template('login.html')


@auth_bp.route('/logout')
@login_required
def logout():

    logout_user()
    return redirect(url_for('auth.login'))


@gerencia_bp.route('/auditoria')
@login_required
def auditoria():
    registros = auditoria_gerencia()
    html = render_template('gerencia/auditoria.html', registros=registros)
    response = make_response(html)
    return response


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(user_id)

    # 🔹 Desactivar caché globalmente
    @app.after_request
    def add_no_cache_headers(response):
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response

    app.register_blueprint(auth_bp)
    app.register_blueprint(gerencia_bp)

    return app
