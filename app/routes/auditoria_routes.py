from app.controllers.auditoria_controller import confirmar_redes_masivo, confirmar_gerencia_masivo
from flask import send_file
import io
import pandas as pd
import xlsxwriter.utility
# Archivo: app/routes/auditoria_routes.py
from flask import Blueprint, render_template, request
from app.controllers.auditoria_controller import auditoria_registros, formatear_numero, confirmar_redes, confirmar_gerencia
from flask_login import login_user, logout_user, login_required, current_user
from flask import request

auditoria_bp = Blueprint('auditoria', __name__)


@auditoria_bp.route('/auditoria/fechas-extremos', methods=['GET'])
@login_required
def fechas_extremos():
    from app.extensions import db
    from sqlalchemy import text
    result = db.session.execute(text('SELECT MIN(fecha_registro_pago) as min_fecha, MAX(fecha_registro_pago) as max_fecha FROM registros_ventas'))
    row = result.fetchone()
    return {'min_fecha': str(row.min_fecha) if row.min_fecha else '', 'max_fecha': str(row.max_fecha) if row.max_fecha else ''}

# Exportar todos los registros a Excel
@auditoria_bp.route('/auditoria/exportar', methods=['GET'])
@login_required
def exportar_auditoria():
    # Solo admin y verificador pueden exportar
    if not hasattr(current_user, 'rol') or current_user.rol.nombre not in ('admin', 'verificador', 'contabilidad'):
        return render_template('403.html'), 403

    # Traer todos los registros con los campos y joins necesarios
    from app.extensions import db
    query = '''
        SELECT
            rv.fecha_registro_pago AS FECHA,
            rv.recibo AS RECIBO,
            ur.nombre AS RESPONSABLE,
            a.nombre AS AREA,
            cc.nombre AS "CTRO. COSTO",
            rv.detalle AS DETALLE,
            e.nombre AS EMPRESA,
            rv.monto AS TOTAL,
            mp.nombre AS "MEDIO DE PAGO"
        FROM registros_ventas rv
        LEFT JOIN usuarios ur ON rv.confirmador_voucher = ur.id
        LEFT JOIN areas a ON rv.area_id = a.id
        LEFT JOIN centros_costo cc ON rv.centro_costo_id = cc.id
        LEFT JOIN empresas e ON rv.empresa_id = e.id
        LEFT JOIN medios_pago mp ON rv.medio_pago_id = mp.id
        ORDER BY rv.fecha_registro_pago ASC
    '''
    with db.engine.connect() as conn:
        df = pd.read_sql_query(query, conn)

    # Formatear fecha con "/"
    if not df.empty:
        df['FECHA'] = pd.to_datetime(df['FECHA']).dt.strftime('%d/%m/%Y')

    # Importar xlsxwriter.utility solo aquí para evitar NameError
    import xlsxwriter.utility

    # Crear Excel en memoria
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Registros')
        workbook = writer.book
        worksheet = writer.sheets['Registros']

        # Aplicar estilo de tabla "Azul, Estilo de tabla claro 9"
        (max_row, max_col) = df.shape
        table_range = xlsxwriter.utility.xl_range(0, 0, max_row, max_col - 1)
        worksheet.add_table(table_range, {
            'columns': [{'header': col} for col in df.columns],
            'style': 'Table Style Light 9',
            'name': 'TablaCaja',
            'autofilter': False
        })

        # Ajustar ancho de columnas
        for i, col in enumerate(df.columns):
            maxlen = max(df[col].astype(str).map(len).max(), len(col)) + 2
            worksheet.set_column(i, i, maxlen)

    output.seek(0)
    return send_file(
        output,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name='Reporte_caja.xlsx'
    )

@auditoria_bp.route('/auditoria/buscar_rango', methods=['POST'])
@login_required
def buscar_rango():
    fecha_desde = request.form.get('fecha_desde')
    fecha_hasta = request.form.get('fecha_hasta')
    registros = auditoria_registros(fecha_desde, fecha_hasta)
    return render_template('auditoria/_tabla_auditoria.html', registros=registros, formatear_numero=formatear_numero)

@auditoria_bp.route('/auditoria/tabla', methods=['POST'])
@login_required
def auditoria_tabla():
    pagina = int(request.form.get('pagina', 1))
    por_pagina = int(request.form.get('por_pagina', 10))
    fecha_desde = request.form.get('fecha_desde')
    fecha_hasta = request.form.get('fecha_hasta')
    estado_confirmacion = request.form.get('estado_confirmacion', 'por_confirmar')
    # Ordenamiento
    orden_campo = request.form.get('orden_campo')
    orden_dir = request.form.get('orden_dir')
    # Traer todos los registros filtrados
    registros_all = auditoria_registros(fecha_desde, fecha_hasta, estado_confirmacion, orden_campo, orden_dir)
    total = len(registros_all)
    inicio = (pagina - 1) * por_pagina
    fin = inicio + por_pagina
    registros = registros_all[inicio:fin]
    hay_mas = fin < total
    html = render_template('auditoria/_tabla_auditoria.html', registros=registros, formatear_numero=formatear_numero)
    return {'html': html, 'hay_mas': hay_mas, 'total': total}

@auditoria_bp.route('/auditoria')
@login_required
def auditoria():
    registros = auditoria_registros()
    return render_template('auditoria/auditoria.html', registros=registros, formatear_numero=formatear_numero)

@auditoria_bp.route('/confirmar_redes/<int:registro_id>', methods=['POST'])
@login_required
def confirmar_redes_route(registro_id):
    return confirmar_redes(registro_id)

@auditoria_bp.route('/confirmar_gerencia/<int:registro_id>', methods=['POST'])
@login_required
def confirmar_gerencia_route(registro_id):
    return confirmar_gerencia(registro_id)

# Confirmación masiva para vendedor
@auditoria_bp.route('/confirmar_redes_masivo', methods=['POST'])
@login_required
def confirmar_redes_masivo_route():
    return confirmar_redes_masivo()

# Confirmación masiva para verificador
@auditoria_bp.route('/confirmar_gerencia_masivo', methods=['POST'])
@login_required
def confirmar_gerencia_masivo_route():
    return confirmar_gerencia_masivo()

# Sincronización de registros desde Xafiro
@auditoria_bp.route('/auditoria/sincronizar_registros', methods=['POST'])
@login_required
def sincronizar_registros_route():
    from app.controllers.auditoria_controller import sincronizar_registros_xafiro
    return sincronizar_registros_xafiro()