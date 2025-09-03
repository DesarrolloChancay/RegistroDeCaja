from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.controllers.archivos_controller import (
    listar_archivos, subir_archivo, descargar_archivo, crear_carpeta,
    eliminar_archivo, renombrar_archivo, obtener_info_archivo, obtener_ruta_navegacion,
    verificar_archivo
)

archivos_bp = Blueprint('archivos', __name__)

# Página principal de gestión de archivos
@archivos_bp.route('/archivos')
@login_required
def pagina_archivos():
    """Muestra la página principal de gestión de archivos"""
    # Verificar permisos básicos de lectura
    if not hasattr(current_user, 'rol') or current_user.rol.nombre not in ['admin', 'vendedor', 'verificador', 'contabilidad']:
        return render_template('403.html'), 403
    
    return render_template('archivos/archivos.html', 
                         titulo="Gestión de Archivos",
                         sessionname=current_user.rol.nombre)

# API endpoints
# Listar archivos y carpetas
archivos_bp.route('/archivos/listar', methods=['GET'])(listar_archivos)

# Subir archivo
archivos_bp.route('/archivos/subir', methods=['POST'])(subir_archivo)

# Descargar archivo
archivos_bp.route('/archivos/descargar/<file_id>', methods=['GET'])(descargar_archivo)

# Crear carpeta
archivos_bp.route('/archivos/crear_carpeta', methods=['POST'])(crear_carpeta)

# Eliminar archivo/carpeta
archivos_bp.route('/archivos/eliminar', methods=['POST'])(eliminar_archivo)

# Renombrar archivo/carpeta
archivos_bp.route('/archivos/renombrar', methods=['POST'])(renombrar_archivo)

# Obtener info de archivo
archivos_bp.route('/archivos/info/<file_id>', methods=['GET'])(obtener_info_archivo)

# Obtener ruta de navegación (breadcrumb)
archivos_bp.route('/archivos/ruta', methods=['GET'])(obtener_ruta_navegacion)

# Verificar archivo (útil para archivos recién subidos)
archivos_bp.route('/archivos/verificar/<file_id>', methods=['GET'])(verificar_archivo)
