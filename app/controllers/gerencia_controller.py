# Archivo: app/controllers/gerencia_controller.py
# Se ha modificado la lógica para recibir y guardar la fecha enviada desde el frontend.

from flask import Blueprint, render_template
from app.models.registro_venta import RegistroVenta
from flask import request, jsonify
from app.extensions import db
from datetime import datetime
from sqlalchemy import text
from zoneinfo import ZoneInfo

gerencia_bp = Blueprint('gerencia', __name__)

@gerencia_bp.route("/auditoria")
def auditoria_gerencia():
    query = """
        SELECT
            rv.id, rv.recibo, rv.monto, rv.detalle, rv.confirmado,
            rv.fecha_registro_pago, rv.fecha_ingreso_cuenta,
            rv.confirmado_redes, rv.fecha_comprobante,
            e.nombre as empresa_nombre,
            eb.nombre as entidad_banco_nombre
        FROM registros_ventas AS rv
        LEFT JOIN empresas AS e ON rv.empresa_id = e.id
        LEFT JOIN entidades_banco AS eb ON rv.entidad_banco_id = eb.id
    """
    with db.engine.connect() as conn:
        result = conn.execute(text(query))
        registros = [dict(row._mapping) for row in result]

    return render_template("gerencia/auditoria.html", registros=registros)

@gerencia_bp.route('/confirmar_redes/<int:registro_id>', methods=['POST'])
def confirmar_redes(registro_id):
    """Confirma un registro desde el área de Redes con la fecha seleccionada."""
    registro = RegistroVenta.query.get(registro_id)
    if not registro:
        return jsonify({"success": False, "error": "Registro no encontrado"}), 404

    if registro.confirmado_redes:
        return jsonify({"success": False, "error": "Ya confirmado por redes"}), 400

    data = request.get_json(silent=True) or {}
    fecha_comprobante_str = data.get("fecha")

    if not fecha_comprobante_str:
        return jsonify({"success": False, "error": "Fecha de comprobante requerida: "}), 400

    try:
        registro.confirmado_redes = True
        registro.fecha_comprobante = datetime.strptime(fecha_comprobante_str, "%Y-%m-%d").date()
        registro.fecha_confirmacion_redes = datetime.now(ZoneInfo("America/Lima"))
        registro.confirmado_por_redes = "verif01"
        db.session.commit()
        return jsonify({"success": True})
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "error": str(e)}), 500

@gerencia_bp.route('/confirmar_gerencia/<int:registro_id>', methods=['POST'])
def confirmar_gerencia(registro_id):
    """Confirma un registro desde Gerencia con la fecha seleccionada."""
    registro = RegistroVenta.query.get(registro_id)
    if not registro:
        return jsonify({"success": False, "error": "Registro no encontrado"}), 404

    if registro.confirmado:
        return jsonify({"success": False, "error": "Ya confirmado por gerencia"}), 400

    data = request.get_json()
    fecha_ingreso_cuenta_str = data.get("fecha")

    if not fecha_ingreso_cuenta_str:
        return jsonify({"success": False, "error": "Fecha de ingreso a cuenta requerida"}), 400

    try:
        registro.confirmado = True
        registro.fecha_ingreso_cuenta = datetime.strptime(fecha_ingreso_cuenta_str, "%Y-%m-%d").date()
        registro.fecha_confirmacion_gerencia = datetime.now(ZoneInfo("America/Lima"))
        registro.confirmado_por_gerencia = "admin01"
        db.session.commit()
        return jsonify({"success": True})
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "error": str(e)}), 500
