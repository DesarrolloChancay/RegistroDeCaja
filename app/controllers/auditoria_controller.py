# Archivo: app/controllers/auditoria_controller.py

from flask import render_template
from app.models.registro_venta import RegistroVenta
from flask import request, jsonify
from app.extensions import db
from datetime import datetime
from sqlalchemy import text
from zoneinfo import ZoneInfo
from flask_login import login_required
from flask_login import current_user

def auditoria_registros(fecha_desde=None, fecha_hasta=None):
    base_query = """
        SELECT
            rv.id, rv.recibo, rv.monto, rv.detalle, rv.confirmado,
            rv.fecha_registro_pago, rv.fecha_ingreso_cuenta,
            rv.confirmado_redes, rv.fecha_comprobante,
            u.nombre as nombre_usuario,
            e.nombre as empresa_nombre,
            eb.nombre as entidad_banco_nombre
        FROM registros_ventas AS rv
        LEFT JOIN empresas AS e ON rv.empresa_id = e.id
        LEFT JOIN usuarios AS u ON rv.confirmado_por_redes = u.id
        LEFT JOIN entidades_banco AS eb ON rv.entidad_banco_id = eb.id
    """
    filtros = []  # Se crea una lista para los filtros
    params = {}  # Se crea un diccionario
    if fecha_desde and not fecha_hasta:
        filtros.append("rv.fecha_registro_pago = :fecha_desde")
        params['fecha_desde'] = fecha_desde
    elif fecha_desde and fecha_hasta:
        filtros.append("rv.fecha_registro_pago BETWEEN :fecha_desde AND :fecha_hasta")
        params['fecha_desde'] = fecha_desde
        params['fecha_hasta'] = fecha_hasta
    if filtros:
        base_query += " WHERE " + " AND ".join(filtros)
    with db.engine.connect() as conn:
        result = conn.execute(text(base_query), params)
        registros = [dict(row._mapping) for row in result]
    return registros

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
        registro.confirmado_por_redes = current_user.id
        db.session.commit()
        return jsonify({"success": True})
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "error": str(e)}), 500

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
        registro.confirmado_por_gerencia = current_user.id
        db.session.commit()
        return jsonify({"success": True})
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "error": str(e)}), 500

def create_titulo(namesession):
    if namesession == 'admin':
        return "Mantenimiento"
    elif namesession == 'verificador':
        return "Gerencia"
    else:
        return "Vendedor"

def formatear_numero(num):
    if num == int(num):
        # Si es entero
        return f"{int(num):,}".replace(",", " ")
    else:
        # Si tiene decimales
        return f"{num:,.2f}".replace(",", " ")
