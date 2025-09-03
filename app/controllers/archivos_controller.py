"""
Controlador para gestión de archivos en Google Drive
Maneja todas las operaciones CRUD de archivos basado en roles de usuario
Usa navegación segura sin exponer folder_ids al frontend
"""
import io
from flask import request, jsonify, send_file, current_app
from flask_login import login_required, current_user
from app.services.google_drive_service import GoogleDriveService
from app.services.navegacion_service import NavegacionService
import logging
from datetime import datetime
from werkzeug.utils import secure_filename
import os

logger = logging.getLogger(__name__)

# Tipos de archivo permitidos por categoría
ALLOWED_EXTENSIONS = {
    'documentos': {'pdf', 'doc', 'docx', 'txt', 'rtf'},
    'imagenes': {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'svg'},
    'hojas_calculo': {'xls', 'xlsx', 'csv'},
    'presentaciones': {'ppt', 'pptx'},
    'archivos': {'zip', 'rar', '7z', 'tar', 'gz'}
}

# Tamaño máximo de archivo (50MB)
MAX_FILE_SIZE = 50 * 1024 * 1024

def allowed_file(filename: str) -> bool:
    """Verifica si el archivo está permitido"""
    if '.' not in filename:
        return False
    
    extension = filename.rsplit('.', 1)[1].lower()
    
    # Verificar si la extensión está en alguna categoría permitida
    for categoria, extensiones in ALLOWED_EXTENSIONS.items():
        if extension in extensiones:
            return True
    
    return False

def verificar_permisos_lectura() -> bool:
    """Verifica si el usuario tiene permisos de lectura"""
    if not current_user.is_authenticated:
        return False
    
    # Todos los roles autenticados pueden leer archivos
    return hasattr(current_user, 'rol') and current_user.rol.nombre in ['admin', 'vendedor', 'verificador', 'contabilidad']

def verificar_permisos_escritura() -> bool:
    """Verifica si el usuario tiene permisos de escritura"""
    if not current_user.is_authenticated:
        return False
    
    # Solo admin y vendedor pueden subir/editar/eliminar archivos
    return hasattr(current_user, 'rol') and current_user.rol.nombre in ['admin', 'vendedor']

def verificar_permisos_admin() -> bool:
    """Verifica si el usuario tiene permisos de administrador"""
    if not current_user.is_authenticated:
        return False
    
    # Solo admin puede crear/eliminar carpetas
    return hasattr(current_user, 'rol') and current_user.rol.nombre == 'admin'

@login_required
def listar_archivos():
    """Lista archivos y carpetas usando navegación segura"""
    try:
        if not verificar_permisos_lectura():
            return jsonify({'success': False, 'error': 'Sin permisos de lectura'}), 403
        
        # Obtener ruta virtual desde el request
        virtual_path = request.args.get('path', '/')
        print(virtual_path)
        
        # Usar el servicio de navegación segura
        navegacion_service = NavegacionService()
        resultado = navegacion_service.navigate_to_path(current_user.id, virtual_path)
        
        if not resultado['success']:
            return jsonify(resultado), 500
        
        # Agregar información del usuario que hace la consulta
        resultado['usuario'] = {
            'id': current_user.id,
            'nombre': current_user.nombre,
            'rol': current_user.rol.nombre,
            'current_path': resultado['virtual_path']
        }
        
        logger.info(f"📋 Usuario {current_user.nombre} listó archivos en ruta: {virtual_path}")
        
        return jsonify(resultado), 200
        
    except Exception as e:
        logger.error(f"❌ Error listando archivos: {str(e)}")
        return jsonify({'success': False, 'error': 'Error interno del servidor'}), 500

@login_required
def subir_archivo():
    """Sube un archivo usando navegación segura"""
    try:
        if not verificar_permisos_escritura():
            return jsonify({'success': False, 'error': 'Sin permisos de escritura'}), 403
        
        # Verificar si hay archivo en el request
        if 'archivo' not in request.files:
            return jsonify({'success': False, 'error': 'No se proporcionó archivo'}), 400
        
        archivo = request.files['archivo']
        
        if archivo.filename == '':
            return jsonify({'success': False, 'error': 'No se seleccionó archivo'}), 400
        
        # Verificar tipo de archivo
        if not allowed_file(archivo.filename):
            return jsonify({'success': False, 'error': 'Tipo de archivo no permitido'}), 400
        
        # Verificar tamaño del archivo
        archivo.seek(0, os.SEEK_END)
        file_size = archivo.tell()
        archivo.seek(0)
        
        if file_size > MAX_FILE_SIZE:
            return jsonify({'success': False, 'error': f'Archivo demasiado grande. Máximo {MAX_FILE_SIZE//1024//1024}MB'}), 400
        
        # Obtener parámetros adicionales
        descripcion = request.form.get('descripcion', '')
        
        # Asegurar nombre de archivo
        filename = secure_filename(archivo.filename)
        
        # Agregar timestamp si es necesario para evitar duplicados
        if request.form.get('agregar_timestamp', 'false').lower() == 'true':
            name, ext = os.path.splitext(filename)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{name}_{timestamp}{ext}"
        
        # Crear un BytesIO del archivo
        archivo_data = io.BytesIO(archivo.read())
        
        # Usar servicio de navegación segura para subir archivo
        navegacion_service = NavegacionService()
        resultado = navegacion_service.upload_file_to_current_path(
            user_id=current_user.id,
            archivo_data=archivo_data,
            filename=filename,
            descripcion=f"Subido por {current_user.nombre} ({current_user.rol.nombre}). {descripcion}".strip()
        )
        
        if not resultado['success']:
            return jsonify(resultado), 500
        
        logger.info(f"📄 Usuario {current_user.nombre} subió archivo: {filename}")
        
        # Agregar información adicional sobre el delay potencial
        resultado['info'] = {
            'upload_successful': True,
            'file_id': resultado['archivo']['id'],
            'delay_notice': 'El archivo puede tomar 1-2 minutos en aparecer en Google Drive web.',
            'verification_available': True
        }
        
        return jsonify(resultado), 200
        
    except Exception as e:
        logger.error(f"❌ Error subiendo archivo: {str(e)}")
        return jsonify({'success': False, 'error': 'Error interno del servidor'}), 500

@login_required
def descargar_archivo(file_id: str):
    """Descarga un archivo de Google Drive"""
    try:
        if not verificar_permisos_lectura():
            return jsonify({'success': False, 'error': 'Sin permisos de lectura'}), 403
        
        # Inicializar servicio de Google Drive
        drive_service = GoogleDriveService()
        
        # Descargar archivo
        resultado = drive_service.descargar_archivo(file_id)
        
        if not resultado['success']:
            return jsonify(resultado), 500
        
        logger.info(f"📥 Usuario {current_user.nombre} descargó archivo: {resultado['filename']}")
        
        # Retornar archivo como descarga
        return send_file(
            resultado['data'],
            as_attachment=True,
            download_name=resultado['filename'],
            mimetype=resultado['mimeType']
        )
        
    except Exception as e:
        logger.error(f"❌ Error descargando archivo: {str(e)}")
        return jsonify({'success': False, 'error': 'Error interno del servidor'}), 500

@login_required
def verificar_archivo(file_id: str):
    """Verifica si un archivo existe en Google Drive (útil para archivos recién subidos)"""
    try:
        if not verificar_permisos_lectura():
            return jsonify({'success': False, 'error': 'Sin permisos de lectura'}), 403
        
        # Inicializar servicio de Google Drive
        drive_service = GoogleDriveService()
        
        # Verificar archivo
        resultado = drive_service.verificar_archivo_existe(file_id)
        
        if not resultado['success']:
            return jsonify(resultado), 500
        
        logger.info(f"🔍 Usuario {current_user.nombre} verificó archivo: {file_id}")
        
        return jsonify(resultado), 200
        
    except Exception as e:
        logger.error(f"❌ Error verificando archivo: {str(e)}")
        return jsonify({'success': False, 'error': 'Error interno del servidor'}), 500

@login_required
def crear_carpeta():
    """Crea una nueva carpeta usando navegación segura"""
    try:
        if not verificar_permisos_admin():
            return jsonify({'success': False, 'error': 'Sin permisos para crear carpetas'}), 403
        
        data = request.get_json()
        
        if not data or 'nombre' not in data:
            return jsonify({'success': False, 'error': 'Nombre de carpeta requerido'}), 400
        
        nombre = data['nombre'].strip()
        if not nombre:
            return jsonify({'success': False, 'error': 'Nombre de carpeta no puede estar vacío'}), 400
        
        # Usar servicio de navegación segura para crear carpeta
        navegacion_service = NavegacionService()
        resultado = navegacion_service.create_folder_in_current_path(current_user.id, nombre)
        
        if not resultado['success']:
            return jsonify(resultado), 400 if 'Ya existe' in resultado.get('error', '') else 500
        
        logger.info(f"📁 Usuario {current_user.nombre} creó carpeta: {nombre}")
        
        return jsonify(resultado), 200
        
    except Exception as e:
        logger.error(f"❌ Error creando carpeta: {str(e)}")
        return jsonify({'success': False, 'error': 'Error interno del servidor'}), 500

@login_required
def eliminar_archivo():
    """Elimina un archivo o carpeta de Google Drive"""
    try:
        if not verificar_permisos_escritura():
            return jsonify({'success': False, 'error': 'Sin permisos de eliminación'}), 403
        
        data = request.get_json()
        
        if not data or 'file_id' not in data:
            return jsonify({'success': False, 'error': 'ID de archivo requerido'}), 400
        
        file_id = data['file_id']
        
        # Inicializar servicio de Google Drive
        drive_service = GoogleDriveService()
        
        # Para carpetas, verificar permisos de admin
        info_resultado = drive_service.obtener_info_archivo(file_id)
        if info_resultado['success']:
            if info_resultado['archivo']['mimeType'] == 'application/vnd.google-apps.folder':
                if not verificar_permisos_admin():
                    return jsonify({'success': False, 'error': 'Sin permisos para eliminar carpetas'}), 403
        
        # Eliminar archivo
        resultado = drive_service.eliminar_archivo(file_id)
        
        if not resultado['success']:
            return jsonify(resultado), 500
        
        logger.info(f"🗑️ Usuario {current_user.nombre} eliminó archivo/carpeta ID: {file_id}")
        
        return jsonify(resultado), 200
        
    except Exception as e:
        logger.error(f"❌ Error eliminando archivo: {str(e)}")
        return jsonify({'success': False, 'error': 'Error interno del servidor'}), 500

@login_required
def renombrar_archivo():
    """Renombra un archivo o carpeta en Google Drive"""
    try:
        if not verificar_permisos_escritura():
            return jsonify({'success': False, 'error': 'Sin permisos de edición'}), 403
        
        data = request.get_json()
        
        if not data or 'file_id' not in data or 'nuevo_nombre' not in data:
            return jsonify({'success': False, 'error': 'ID de archivo y nuevo nombre requeridos'}), 400
        
        file_id = data['file_id']
        nuevo_nombre = data['nuevo_nombre'].strip()
        
        if not nuevo_nombre:
            return jsonify({'success': False, 'error': 'El nuevo nombre no puede estar vacío'}), 400
        
        # Inicializar servicio de Google Drive
        drive_service = GoogleDriveService()
        
        # Para carpetas, verificar permisos de admin
        info_resultado = drive_service.obtener_info_archivo(file_id)
        if info_resultado['success']:
            if info_resultado['archivo']['mimeType'] == 'application/vnd.google-apps.folder':
                if not verificar_permisos_admin():
                    return jsonify({'success': False, 'error': 'Sin permisos para renombrar carpetas'}), 403
        
        # Renombrar archivo
        resultado = drive_service.renombrar_archivo(file_id, nuevo_nombre)
        
        if not resultado['success']:
            return jsonify(resultado), 500
        
        logger.info(f"✏️ Usuario {current_user.nombre} renombró archivo a: {nuevo_nombre}")
        
        return jsonify(resultado), 200
        
    except Exception as e:
        logger.error(f"❌ Error renombrando archivo: {str(e)}")
        return jsonify({'success': False, 'error': 'Error interno del servidor'}), 500

@login_required
def obtener_info_archivo(file_id: str):
    """Obtiene información detallada de un archivo"""
    try:
        if not verificar_permisos_lectura():
            return jsonify({'success': False, 'error': 'Sin permisos de lectura'}), 403
        
        # Inicializar servicio de Google Drive
        drive_service = GoogleDriveService()
        
        # Obtener información
        resultado = drive_service.obtener_info_archivo(file_id)
        
        if not resultado['success']:
            return jsonify(resultado), 500
        
        return jsonify(resultado), 200
        
    except Exception as e:
        logger.error(f"❌ Error obteniendo info del archivo: {str(e)}")
        return jsonify({'success': False, 'error': 'Error interno del servidor'}), 500

@login_required
def obtener_ruta_navegacion():
    """Obtiene información de navegación (breadcrumb) desde el backend"""
    try:
        if not verificar_permisos_lectura():
            return jsonify({'success': False, 'error': 'Sin permisos de lectura'}), 403
        
        navegacion_service = NavegacionService()
        current_path = navegacion_service.get_current_path(current_user.id)
        breadcrumb = navegacion_service._generate_breadcrumb(current_path)
        
        return jsonify({
            'success': True,
            'current_path': current_path,
            'breadcrumb': breadcrumb
        }), 200
        
    except Exception as e:
        logger.error(f"❌ Error obteniendo ruta de navegación: {str(e)}")
        return jsonify({'success': False, 'error': 'Error interno del servidor'}), 500
