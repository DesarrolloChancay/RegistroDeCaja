"""
Servicio de navegación segura para Google Drive
Maneja rutas virtuales sin exponer folder_ids al frontend
"""
import logging
from typing import Dict, List, Optional, Tuple
from flask import session
from app.services.google_drive_service import GoogleDriveService

logger = logging.getLogger(__name__)

class NavegacionService:
    def __init__(self):
        """Inicializa el servicio de navegación"""
        self.drive_service = GoogleDriveService()
        
    def _get_session_key(self, user_id: int) -> str:
        """Genera clave de sesión para el mapeo de rutas del usuario"""
        return f"navigation_map_{user_id}"
    
    def _get_navigation_map(self, user_id: int) -> Dict[str, str]:
        """Obtiene el mapeo de rutas virtuales a folder_ids reales"""
        session_key = self._get_session_key(user_id)
        if session_key not in session:
            # Inicializar con la ruta raíz
            session[session_key] = {
                '/': self.drive_service.get_root_folder_id()
            }
        return session[session_key]
    
    def _save_navigation_map(self, user_id: int, navigation_map: Dict[str, str]):
        """Guarda el mapeo de navegación en la sesión"""
        session_key = self._get_session_key(user_id)
        session[session_key] = navigation_map
        session.permanent = True
    
    def _add_to_navigation_map(self, user_id: int, virtual_path: str, folder_id: str):
        """Agrega una nueva ruta al mapeo de navegación"""
        navigation_map = self._get_navigation_map(user_id)
        navigation_map[virtual_path] = folder_id
        self._save_navigation_map(user_id, navigation_map)
    
    def get_folder_id_from_path(self, user_id: int, virtual_path: str) -> Optional[str]:
        """Convierte una ruta virtual a folder_id real"""
        if not virtual_path:
            virtual_path = '/'
        
        navigation_map = self._get_navigation_map(user_id)
        return navigation_map.get(virtual_path)
    
    def get_current_path(self, user_id: int) -> str:
        """Obtiene la ruta actual del usuario"""
        return session.get(f"current_path_{user_id}", '/')
    
    def set_current_path(self, user_id: int, virtual_path: str):
        """Establece la ruta actual del usuario"""
        session[f"current_path_{user_id}"] = virtual_path
        session.permanent = True
    
    def navigate_to_path(self, user_id: int, virtual_path: str) -> Dict:
        """
        Navega a una ruta virtual específica
        
        Args:
            user_id: ID del usuario
            virtual_path: Ruta virtual (ej: '/', '/carpeta1', '/carpeta1/subcarpeta')
            
        Returns:
            Dict con el resultado de la navegación
        """
        try:
            # Normalizar ruta
            if not virtual_path:
                virtual_path = '/'
            
            # Obtener folder_id real
            folder_id = self.get_folder_id_from_path(user_id, virtual_path)
            
            if folder_id is None:
                logger.warning(f"Ruta no encontrada en el mapeo: {virtual_path}")
                return {
                    'success': False,
                    'error': 'Ruta no válida',
                    'virtual_path': virtual_path
                }
            
            # Listar archivos usando el folder_id real
            resultado = self.drive_service.listar_archivos(folder_id, incluir_carpetas=True)
            
            if not resultado['success']:
                return resultado
            
            # Actualizar ruta actual
            self.set_current_path(user_id, virtual_path)
            
            # Procesar carpetas para agregar rutas virtuales
            carpetas_procesadas = []
            for carpeta in resultado['carpetas']:
                # Crear ruta virtual para la subcarpeta
                if virtual_path == '/':
                    nueva_ruta = f"/{carpeta['name']}"
                else:
                    nueva_ruta = f"{virtual_path}/{carpeta['name']}"
                
                # Agregar al mapeo de navegación
                self._add_to_navigation_map(user_id, nueva_ruta, carpeta['id'])
                
                # Crear objeto carpeta con ruta virtual
                carpeta_procesada = carpeta.copy()
                carpeta_procesada['virtual_path'] = nueva_ruta
                carpetas_procesadas.append(carpeta_procesada)
            
            # Generar breadcrumb
            breadcrumb = self._generate_breadcrumb(virtual_path)
            
            logger.info(f"👤 Usuario {user_id} navegó a: {virtual_path}")
            
            return {
                'success': True,
                'carpetas': carpetas_procesadas,
                'archivos': resultado['archivos'],
                'total_carpetas': len(carpetas_procesadas),
                'total_archivos': len(resultado['archivos']),
                'virtual_path': virtual_path,
                'breadcrumb': breadcrumb,
                'usuario': {
                    'current_path': virtual_path
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Error navegando a {virtual_path}: {str(e)}")
            return {
                'success': False,
                'error': f'Error de navegación: {str(e)}',
                'virtual_path': virtual_path
            }
    
    def _generate_breadcrumb(self, virtual_path: str) -> List[Dict]:
        """Genera el breadcrumb para una ruta virtual"""
        if virtual_path == '/':
            return [{'name': 'Inicio', 'path': '/', 'is_current': True}]
        
        breadcrumb = [{'name': 'Inicio', 'path': '/', 'is_current': False}]
        
        # Dividir la ruta en partes
        parts = [part for part in virtual_path.split('/') if part]
        current_path = ''
        
        for i, part in enumerate(parts):
            current_path += f"/{part}"
            is_current = (i == len(parts) - 1)
            
            breadcrumb.append({
                'name': part,
                'path': current_path,
                'is_current': is_current
            })
        
        return breadcrumb
    
    def create_folder_in_current_path(self, user_id: int, folder_name: str) -> Dict:
        """
        Crea una carpeta en la ruta actual del usuario
        
        Args:
            user_id: ID del usuario
            folder_name: Nombre de la nueva carpeta
            
        Returns:
            Dict con el resultado de la operación
        """
        try:
            current_path = self.get_current_path(user_id)
            current_folder_id = self.get_folder_id_from_path(user_id, current_path)
            
            if not current_folder_id:
                return {
                    'success': False,
                    'error': 'No se pudo determinar la carpeta actual'
                }
            
            # Crear la carpeta
            resultado = self.drive_service.crear_carpeta(folder_name, current_folder_id)
            
            if resultado['success']:
                # Agregar la nueva carpeta al mapeo de navegación
                if current_path == '/':
                    nueva_ruta = f"/{folder_name}"
                else:
                    nueva_ruta = f"{current_path}/{folder_name}"
                
                self._add_to_navigation_map(user_id, nueva_ruta, resultado['folder']['id'])
                
                logger.info(f"📁 Usuario {user_id} creó carpeta: {nueva_ruta}")
            
            return resultado
            
        except Exception as e:
            logger.error(f"❌ Error creando carpeta: {str(e)}")
            return {
                'success': False,
                'error': f'Error creando carpeta: {str(e)}'
            }
    
    def upload_file_to_current_path(self, user_id: int, archivo_data, filename: str, descripcion: str = '') -> Dict:
        """
        Sube un archivo a la ruta actual del usuario
        
        Args:
            user_id: ID del usuario
            archivo_data: Datos del archivo
            filename: Nombre del archivo
            descripcion: Descripción del archivo
            
        Returns:
            Dict con el resultado de la operación
        """
        try:
            current_path = self.get_current_path(user_id)
            current_folder_id = self.get_folder_id_from_path(user_id, current_path)
            
            if not current_folder_id:
                return {
                    'success': False,
                    'error': 'No se pudo determinar la carpeta actual'
                }
            
            # Subir el archivo
            resultado = self.drive_service.subir_archivo(
                archivo_data=archivo_data,
                nombre_archivo=filename,
                parent_folder_id=current_folder_id,
                descripcion=descripcion
            )
            
            if resultado['success']:
                logger.info(f"📄 Usuario {user_id} subió archivo: {filename} en {current_path}")
            
            return resultado
            
        except Exception as e:
            logger.error(f"❌ Error subiendo archivo: {str(e)}")
            return {
                'success': False,
                'error': f'Error subiendo archivo: {str(e)}'
            }
    
    def reset_navigation(self, user_id: int):
        """Reinicia la navegación del usuario a la raíz"""
        session_key = self._get_session_key(user_id)
        if session_key in session:
            del session[session_key]
        
        current_path_key = f"current_path_{user_id}"
        if current_path_key in session:
            del session[current_path_key]
        
        logger.info(f"🔄 Navegación reiniciada para usuario {user_id}")
