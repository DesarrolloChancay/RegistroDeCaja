from flask import Blueprint, render_template
from app.models.registro_venta import RegistroVenta
from flask import request, jsonify
from app.extensions import db
from datetime import datetime

gerencia_bp = Blueprint('gerencia', __name__)

@gerencia_bp.route("/auditoria")
def auditoria_gerencia():
    registros = RegistroVenta.query.all()
    return render_template("gerencia/auditoria.html", registros=registros)

@gerencia_bp.route('/confirmar_redes/<int:registro_id>', methods=['POST'])
def confirmar_redes(registro_id):
    data = request.get_json()
    fecha_str = data.get("fecha")

    if not fecha_str:
        return jsonify({"success": False, "error": "Fecha requerida"}), 400

    registro = RegistroVenta.query.get(registro_id)
    if not registro:
        return jsonify({"success": False, "error": "Registro no encontrado"}), 404

    if registro.confirmado_redes:
        return jsonify({"success": False, "error": "Ya confirmado por redes"}), 400

    try:
        registro.confirmado_redes = True
        registro.fecha_confirmacion_redes = datetime.strptime(fecha_str, "%Y-%m-%d")
        registro.confirmado_por_redes = "verif01"  # Temporalmente fijo
        db.session.commit()
        return jsonify({"success": True})
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "error": str(e)}), 500
