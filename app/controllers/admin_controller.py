
# Archivo: app/controllers/admin_controller.py

from flask import render_template, request, jsonify
from flask_login import login_required, current_user
from app.models.admin import Admin
from app.controllers.auditoria_controller import auditoria_registros, formatear_numero
from app.extensions import db
from app.models.Usuario import Usuario
from app.models.registro_venta import RegistroVenta
from sqlalchemy import text
from zoneinfo import ZoneInfo
from datetime import datetime

# Decorador para restringir solo a admin
def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not hasattr(current_user, 'rol') or current_user.rol.nombre != 'admin':
            return render_template('403.html'), 403
        return f(*args, **kwargs)
    return decorated_function

@login_required
@admin_required
def editar_fecha_voucher():
    registro_id = request.form.get('id')
    nueva_fecha = request.form.get('fecha')
    if not registro_id or not nueva_fecha:
        return jsonify({'success': False, 'error': 'Datos incompletos'}), 400
    reg = RegistroVenta.query.get(registro_id)
    if not reg:
        return jsonify({'success': False, 'error': 'Registro no encontrado'}), 404
    try:
        reg.fecha_comprobante = datetime.strptime(nueva_fecha, "%Y-%m-%d").date()
        reg.vendedor_id = current_user.id
        # reg.fecha_edicion_admin = datetime.now(ZoneInfo("America/Lima"))  # <-- Descomentar cuando exista la columna
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@login_required
@admin_required
def editar_fecha_ingreso():
    registro_id = request.form.get('id')
    nueva_fecha = request.form.get('fecha')
    if not registro_id or not nueva_fecha:
        return jsonify({'success': False, 'error': 'Datos incompletos'}), 400
    reg = RegistroVenta.query.get(registro_id)
    if not reg:
        return jsonify({'success': False, 'error': 'Registro no encontrado'}), 404
    try:
        reg.fecha_ingreso_cuenta = datetime.strptime(nueva_fecha, "%Y-%m-%d").date()
        reg.vendedor_id = current_user.id
        # reg.fecha_edicion_admin = datetime.now(ZoneInfo("America/Lima"))  # <-- Descomentar cuando exista la columna
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@login_required
@admin_required
def admin_mantenimiento():
    return render_template('admin/mantenimiento.html')

# --- AJAX: Empresas ---
@login_required
@admin_required
def tabla_empresas():
    pagina = int(request.args.get('pagina', 1))
    por_pagina = 10
    empresas = db.session.execute(text('SELECT id, nombre FROM empresas ORDER BY id LIMIT :lim OFFSET :off'), {'lim': por_pagina, 'off': (pagina-1)*por_pagina}).fetchall()
    total = db.session.execute(text('SELECT COUNT(*) FROM empresas')).scalar()
    hay_mas = (pagina * por_pagina) < total
    filas = [dict(row._mapping) for row in empresas]
    return render_template('admin/_tabla_generica.html',
        titulo_tabla='Empresas', tab='empresas', columnas=['id','nombre'], filas=filas,
        campos=[{'nombre':'nombre','placeholder':'Nombre empresa'}], pagina=pagina, hay_mas=hay_mas)

@login_required
@admin_required
def agregar_empresa():
    nombre = request.form.get('nombre')
    if not nombre:
        return jsonify({'success': False, 'error': 'Nombre requerido'})
    try:
        db.session.execute(text('INSERT INTO empresas (nombre) VALUES (:nombre)'), {'nombre': nombre})
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})

# --- AJAX: Centros de Costo ---
@login_required
@admin_required
def tabla_centros_costo():
    pagina = int(request.args.get('pagina', 1))
    por_pagina = 10
    centros = db.session.execute(text('SELECT id, nombre FROM centros_costo ORDER BY id LIMIT :lim OFFSET :off'), {'lim': por_pagina, 'off': (pagina-1)*por_pagina}).fetchall()
    total = db.session.execute(text('SELECT COUNT(*) FROM centros_costo')).scalar()
    hay_mas = (pagina * por_pagina) < total
    filas = [dict(row._mapping) for row in centros]
    return render_template('admin/_tabla_generica.html',
        titulo_tabla='Centros de Costo', tab='centros_costo', columnas=['id','nombre'], filas=filas,
        campos=[{'nombre':'nombre','placeholder':'Nombre centro de costo'}], pagina=pagina, hay_mas=hay_mas)

@login_required
@admin_required
def agregar_centro_costo():
    nombre = request.form.get('nombre')
    if not nombre:
        return jsonify({'success': False, 'error': 'Nombre requerido'})
    try:
        db.session.execute(text('INSERT INTO centros_costo (nombre) VALUES (:nombre)'), {'nombre': nombre})
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})

# --- AJAX: Usuarios ---
@login_required
@admin_required
def tabla_usuarios():
    """
    Renderiza la tabla paginada de usuarios para el panel de administración.
    """
    pagina = int(request.args.get('pagina', 1))
    por_pagina = 10
    usuarios = db.session.execute(
        text(
            'SELECT u.id, u.nombre, u.correo, r.nombre AS rol FROM usuarios AS u'
            ' LEFT JOIN roles AS r ON u.rol_id = r.id '
            'ORDER BY u.id LIMIT :lim OFFSET :off'
        ),
        {'lim': por_pagina, 'off': (pagina - 1) * por_pagina}
    ).fetchall()
    total = db.session.execute(
        text('SELECT COUNT(*) FROM usuarios')
    ).scalar()
    hay_mas = (pagina * por_pagina) < total
    filas = [dict(row._mapping) for row in usuarios]
    return render_template(
        'admin/_tabla_generica.html',
        titulo_tabla='Usuarios',
        tab='usuarios',
        columnas=['id', 'nombre', 'correo', 'rol'],
        filas=filas,
        campos=[
            {'nombre': 'id', 'placeholder': 'ID usuario'},
            {'nombre': 'nombre', 'placeholder': 'Nombre'},
            {'nombre': 'correo', 'placeholder': 'Correo'},
            {'nombre': 'rol', 'placeholder': 'Rol'},
            {'nombre': 'contrasena', 'placeholder': 'Contraseña'}
        ],
        pagina=pagina,
        hay_mas=hay_mas
    )

@login_required
@admin_required
def agregar_usuario():
    idu = request.form.get('id')
    nombre = request.form.get('nombre')
    correo = request.form.get('correo')
    contrasena = request.form.get('contrasena')
    rol = request.form.get('rol')
    if not (idu and nombre and correo and contrasena and rol):
        return jsonify({'success': False, 'error': 'Todos los campos son requeridos'})
    # Mapear nombre de rol a rol_id
    rol_map = {'admin': 1, 'vendedor': 2, 'verificador': 3}
    rol_id = rol_map.get(rol)
    if not rol_id:
        return jsonify({'success': False, 'error': 'Rol inválido'})
    try:
        db.session.execute(text('INSERT INTO usuarios (id, nombre, correo, contrasena, rol_id) VALUES (:id, :nombre, :correo, :contrasena, :rol_id)'), {'id': idu, 'nombre': nombre, 'correo': correo, 'contrasena': contrasena, 'rol_id': rol_id})
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})

# --- AJAX: Entidades de Pago ---
@login_required
@admin_required
def tabla_entidades_banco():
    pagina = int(request.args.get('pagina', 1))
    por_pagina = 10
    entidades = db.session.execute(text('SELECT id, nombre FROM entidades_banco ORDER BY id LIMIT :lim OFFSET :off'), {'lim': por_pagina, 'off': (pagina-1)*por_pagina}).fetchall()
    total = db.session.execute(text('SELECT COUNT(*) FROM entidades_banco')).scalar()
    hay_mas = (pagina * por_pagina) < total
    filas = [dict(row._mapping) for row in entidades]
    return render_template('admin/_tabla_generica.html',
        titulo_tabla='Entidades de Pago', tab='entidades_banco', columnas=['id','nombre'], filas=filas,
        campos=[{'nombre':'nombre','placeholder':'Nombre entidad'}], pagina=pagina, hay_mas=hay_mas)

@login_required
@admin_required
def agregar_entidad_banco():
    nombre = request.form.get('nombre')
    if not nombre:
        return jsonify({'success': False, 'error': 'Nombre requerido'})
    try:
        db.session.execute(text('INSERT INTO entidades_banco (nombre) VALUES (:nombre)'), {'nombre': nombre})
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})

# --- AJAX: Medios de Pago ---
@login_required
@admin_required
def tabla_medios_pago():
    pagina = int(request.args.get('pagina', 1))
    por_pagina = 10
    medios = db.session.execute(text('SELECT id, nombre FROM medios_pago ORDER BY id LIMIT :lim OFFSET :off'), {'lim': por_pagina, 'off': (pagina-1)*por_pagina}).fetchall()
    total = db.session.execute(text('SELECT COUNT(*) FROM medios_pago')).scalar()
    hay_mas = (pagina * por_pagina) < total
    filas = [dict(row._mapping) for row in medios]
    return render_template('admin/_tabla_generica.html',
        titulo_tabla='Medios de Pago', tab='medios_pago', columnas=['id','nombre'], filas=filas,
        campos=[{'nombre':'nombre','placeholder':'Nombre medio de pago'}], pagina=pagina, hay_mas=hay_mas)

@login_required
@admin_required
def agregar_medio_pago():
    nombre = request.form.get('nombre')
    if not nombre:
        return jsonify({'success': False, 'error': 'Nombre requerido'})
    try:
        db.session.execute(text('INSERT INTO medios_pago (nombre) VALUES (:nombre)'), {'nombre': nombre})
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})
