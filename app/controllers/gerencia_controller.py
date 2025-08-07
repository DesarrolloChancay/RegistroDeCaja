from flask import Blueprint, render_template
from app.models.registro_venta import RegistroVenta

gerencia_bp = Blueprint('gerencia', __name__)

@gerencia_bp.route("/auditoria")
def auditoria_gerencia():
    registros = RegistroVenta.query.all()
    return render_template("gerencia/auditoria.html", registros=registros)
