
# Archivo: app/controllers/auditoria_controller.py

from app.models.registro_venta import RegistroVenta
from flask import request, jsonify
from app.extensions import db
from datetime import datetime
from sqlalchemy import text
from zoneinfo import ZoneInfo
from flask_login import current_user
from flask_login import login_required
from sqlalchemy.orm import sessionmaker

def auditoria_registros(fecha_desde=None, fecha_hasta=None, estado_confirmacion=None, orden_campo=None, orden_dir=None):
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
        LEFT JOIN usuarios AS u ON rv.confirmador_voucher = u.id
        LEFT JOIN entidades_banco AS eb ON rv.entidad_banco_id = eb.id
    """
    filtros = []
    params = {}
    if fecha_desde and not fecha_hasta:
        filtros.append("rv.fecha_registro_pago = :fecha_desde")
        params['fecha_desde'] = fecha_desde
    elif fecha_desde and fecha_hasta:
        filtros.append("rv.fecha_registro_pago BETWEEN :fecha_desde AND :fecha_hasta")
        params['fecha_desde'] = fecha_desde
        params['fecha_hasta'] = fecha_hasta
    # Filtro por estado de confirmación y rol
    from flask_login import current_user
    rol = getattr(current_user, 'rol', None)
    nombre_rol = getattr(rol, 'nombre', None)
    if estado_confirmacion == 'por_confirmar':
        if nombre_rol == 'vendedor':
            # Solo los que no están confirmados por redes (vendedor)
            filtros.append("(rv.confirmado_redes = 0 OR rv.confirmado_redes IS NULL)")
        elif nombre_rol == 'verificador':
            # Solo los que ya fueron confirmados por redes pero no por gerencia
            filtros.append("(rv.confirmado_redes = 1 AND (rv.confirmado = 0 OR rv.confirmado IS NULL))")
        else:
            # admin: todos los que no están confirmados por gerencia
            filtros.append("(rv.confirmado = 0 OR rv.confirmado IS NULL)")
    elif estado_confirmacion == 'confirmados':
        if nombre_rol == 'vendedor':
            # Solo los que no están confirmados por redes (vendedor)
            filtros.append("(rv.confirmado_redes = 1)")
        elif nombre_rol == 'verificador':
            # Solo los que ya fueron confirmados por redes pero no por gerencia
            filtros.append("(rv.confirmado_redes = 1 AND (rv.confirmado = 1))")
        else:
            # admin: todos los que no están confirmados por gerencia
            filtros.append("(rv.confirmado_redes = 1 AND rv.confirmado = 1)")
    if filtros:
        base_query += " WHERE " + " AND ".join(filtros)
    # Orden dinámico
    campo = None
    if orden_campo in ['fecha_confirmacion_redes', 'fecha_confirmacion_gerencia', 'fecha_registro_pago']:
        campo = orden_campo
    else:
        # fallback por rol y estado
        if estado_confirmacion == 'por_confirmar':
            if nombre_rol == 'admin' or nombre_rol == 'verificador':
                campo = 'fecha_confirmacion_redes'
            else:
                campo = 'fecha_registro_pago'
        elif estado_confirmacion == 'confirmados':
            if nombre_rol == 'vendedor':
                campo = 'fecha_confirmacion_redes'
            elif nombre_rol == 'verificador' or nombre_rol == 'admin':
                campo = 'fecha_confirmacion_gerencia'
    direccion = 'DESC'
    if orden_dir and str(orden_dir).lower() in ['asc', 'desc']:
        direccion = orden_dir.upper()
    if campo:
        base_query += f" ORDER BY rv.{campo} {direccion}"
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

    from sqlalchemy.orm import sessionmaker
    try:
        ip = obtener_ip()
        motivo = None  # Para todos los roles, motivo es None
        Session = sessionmaker(bind=db.engine)
        with db.engine.begin() as connection:
            session = Session(bind=connection)
            connection.execute(
                text("CALL SetAuditContext(:user_id, :reason, :ip)"),
                {"user_id": current_user.id, "reason": motivo, "ip": ip}
            )
            registro = session.get(RegistroVenta, registro_id)
            registro.confirmado_redes = True
            # Si es admin o vendedor, permitir fecha y hora
            try:
                registro.fecha_comprobante = datetime.strptime(fecha_comprobante_str, "%Y-%m-%d %H:%M")
            except ValueError as e:
                # Si falla, intentar solo la fecha y mostrar error específico
                try:
                    fecha_sin_hora = datetime.strptime(fecha_comprobante_str, "%Y-%m-%d")
                    if current_user.rol.nombre in ['admin', 'vendedor']:
                        return jsonify({"success": False, "error": "El formato de fecha y hora debe ser YYYY-MM-DD HH:MM"}), 400
                    registro.fecha_comprobante = fecha_sin_hora.replace(hour=0, minute=0)
                except ValueError:
                    return jsonify({"success": False, "error": "Formato de fecha inválido. Use YYYY-MM-DD HH:MM"}), 400
            registro.fecha_confirmacion_redes = datetime.now(ZoneInfo("America/Lima"))
            registro.confirmador_voucher = current_user.id
            session.commit()
            connection.execute(text("CALL ClearAuditContext()"))
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

    from sqlalchemy.orm import sessionmaker
    try:
        ip = obtener_ip()
        motivo = None  # Para todos los roles, motivo es None
        Session = sessionmaker(bind=db.engine)
        with db.engine.begin() as connection:
            session = Session(bind=connection)
            connection.execute(
                text("CALL SetAuditContext(:user_id, :reason, :ip)"),
                {"user_id": current_user.id, "reason": motivo, "ip": ip}
            )
            registro = session.get(RegistroVenta, registro_id)
            registro.confirmado = True
            registro.fecha_ingreso_cuenta = datetime.strptime(fecha_ingreso_cuenta_str, "%Y-%m-%d").date()
            registro.fecha_confirmacion_gerencia = datetime.now(ZoneInfo("America/Lima"))
            registro.confirmador_cuenta = current_user.id
            session.commit()
            connection.execute(text("CALL ClearAuditContext()"))
        return jsonify({"success": True})
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "error": str(e)}), 500

def create_titulo(namesession):
    if namesession == 'admin':
        return "Mantenimiento"
    elif namesession == 'verificador':
        return "Gerencia"
    elif namesession == 'contabilidad':
        return "Contabilidad"
    else:
        return "Vendedor"

def formatear_numero(num):
    if num == int(num):
        # Si es entero
        return f"{int(num):,}".replace(",", " ")
    else:
        # Si tiene decimales
        return f"{num:,.2f}".replace(",", " ")

def obtener_ip():
    if request.headers.get('X-Forwarded-For'):
        ip = request.headers.get('X-Forwarded-For').split(',')[0].strip()
    else:
        ip = request.remote_addr or ''
    return ip

# --- Confirmación masiva para vendedor y verificador ---
def confirmar_redes_masivo():
    from flask import request, jsonify
    from .auditoria_controller import obtener_ip
    if not hasattr(current_user, 'rol') or current_user.rol.nombre != 'vendedor':
        return jsonify({'success': False, 'error': 'No autorizado'}), 403
    try:
        data = request.get_json()
        registros = data.get('registros', [])
        if not registros:
            return jsonify({'success': False, 'error': 'No hay registros'}), 400
        ip = obtener_ip()
        Session = sessionmaker(bind=db.engine)
        with db.engine.begin() as connection:
            session = Session(bind=connection)
            for reg in registros:
                id = reg.get('id')
                fecha = reg.get('fecha')
                if not id or not fecha:
                    continue
                connection.execute(text("CALL SetAuditContext(:user_id, :reason, :ip)"),
                    {"user_id": current_user.id, "reason": "Confirmación masiva redes", "ip": ip})
                rv = session.get(RegistroVenta, id)
                if rv and not rv.confirmado_redes:
                    try:
                        # Para admin y vendedor, requerir fecha y hora
                        rv.fecha_comprobante = datetime.strptime(fecha, "%Y-%m-%d %H:%M")
                    except ValueError as e:
                        try:
                            fecha_sin_hora = datetime.strptime(fecha, "%Y-%m-%d")
                            if current_user.rol.nombre in ['admin', 'vendedor']:
                                raise ValueError("El formato de fecha y hora debe ser YYYY-MM-DD HH:MM")
                            rv.fecha_comprobante = fecha_sin_hora.replace(hour=0, minute=0)
                        except ValueError as ve:
                            return jsonify({"success": False, "error": str(ve)}), 400
                    rv.confirmado_redes = 1
                    rv.confirmador_voucher = current_user.id
                    rv.fecha_confirmacion_redes = datetime.now(ZoneInfo("America/Lima"))
            session.commit()
            connection.execute(text("CALL ClearAuditContext()"))
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

def confirmar_gerencia_masivo():
    from flask import request, jsonify
    from .auditoria_controller import obtener_ip
    if not hasattr(current_user, 'rol') or current_user.rol.nombre != 'verificador':
        return jsonify({'success': False, 'error': 'No autorizado'}), 403
    try:
        data = request.get_json()
        registros = data.get('registros', [])
        if not registros:
            return jsonify({'success': False, 'error': 'No hay registros'}), 400
        ip = obtener_ip()
        Session = sessionmaker(bind=db.engine)
        with db.engine.begin() as connection:
            session = Session(bind=connection)
            for reg in registros:
                id = reg.get('id')
                fecha = reg.get('fecha')
                if not id or not fecha:
                    continue
                connection.execute(text("CALL SetAuditContext(:user_id, :reason, :ip)"),
                    {"user_id": current_user.id, "reason": "Confirmación masiva gerencia", "ip": ip})
                rv = session.get(RegistroVenta, id)
                if rv and not rv.confirmado:
                    rv.fecha_ingreso_cuenta = datetime.strptime(fecha, "%Y-%m-%d").date()
                    rv.confirmado = 1
                    rv.confirmador_cuenta = current_user.id
                    rv.fecha_confirmacion_gerencia = datetime.now(ZoneInfo("America/Lima"))
            session.commit()
            connection.execute(text("CALL ClearAuditContext()"))
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

def sincronizar_registros_xafiro():
    """
    Sincroniza registros desde Xafiro utilizando el servicio de sincronización
    """
    from app.services.sincronizacion_service import SincronizacionService
    import logging
    
    # Configurar logging para esta función
    logger = logging.getLogger(__name__)
    
    # Verificar permisos (solo admin y vendedor)
    if not hasattr(current_user, 'rol') or current_user.rol.nombre not in ['admin', 'vendedor']:
        logger.warning(f"Usuario {current_user.id} intentó sincronizar sin permisos")
        return jsonify({'success': False, 'error': 'No autorizado'}), 403
    
    try:
        logger.info(f"Usuario {current_user.id} ({current_user.rol.nombre}) inició sincronización")
        
        # Obtener fecha del request o usar ayer por defecto
        data = request.get_json() if request.is_json else {}
        fecha = data.get('fecha') if data else None
        
        # Ejecutar sincronización
        resultado = SincronizacionService.sincronizar_registros(fecha)
        
        if resultado['success']:
            logger.info(f"Sincronización exitosa: {resultado['total_insertados']} registros insertados")
            return jsonify(resultado), 200
        else:
            logger.error(f"Error en sincronización: {resultado['message']}")
            return jsonify(resultado), 400
            
    except Exception as e:
        logger.error(f"Excepción durante sincronización: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error en sincronización: {str(e)}',
            'total_extraidos': 0,
            'total_insertados': 0,
            'errores': [str(e)]
        }), 500