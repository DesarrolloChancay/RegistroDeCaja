# Sistema de Gestión de Archivos - Google Drive

## 📋 Descripción

Sistema completo de gestión de archivos integrado con Google Drive API usando cuenta de servicio. Permite subir, descargar, navegar y gestionar archivos de manera segura con control de acceso por roles.

## 🔧 Características Principales

### ✅ Funcionalidades Implementadas

- **📁 Navegación completa**: Navegar por carpetas y subcarpetas
- **📤 Subida de archivos**: Cargar archivos a cualquier carpeta
- **📥 Descarga de archivos**: Descargar archivos existentes
- **🗂️ Gestión de carpetas**: Crear y navegar carpetas
- **🔐 Control de acceso por roles**:
  - **Admin**: Acceso completo (CRUD)
  - **Vendedor**: Lectura y escritura de archivos
  - **Verificador/Contabilidad**: Solo lectura
- **🛡️ Navegación segura**: Rutas virtuales sin exposer folder_ids
- **🔄 Consulta híbrida**: Solución para problemas de indexación de Google Drive API

### 🚀 Solución Técnica Destacada

**Problema resuelto**: La API de Google Drive tiene inconsistencias de indexación donde archivos existen pero no aparecen en consultas normales.

**Solución implementada**: Sistema híbrido que combina dos sintaxis de consulta:
- Consulta normal: `'folder_id' in parents`
- Consulta alternativa: `parents in 'folder_id'`

Esto garantiza que todos los archivos se muestren correctamente en la navegación.

## 📂 Estructura de Archivos

```
app/
├── services/
│   ├── google_drive_service.py    # Servicio principal de Google Drive
│   └── navegacion_service.py      # Navegación segura con rutas virtuales
├── controllers/
│   └── archivos_controller.py     # Controlador con validación de roles
├── routes/
│   └── archivos_routes.py         # Rutas de la API de archivos
└── templates/archivos/
    └── archivos.html              # Interfaz de usuario
```

## 🔐 Configuración de Seguridad

### Variables de Entorno (.env)
```
ROOT_FOLDER_ID=tu_folder_id_del_shared_drive
```

### Cuenta de Servicio
- Archivo: `google_service_account.json`
- Requiere configuración de Shared Drive
- Permisos de editor en el Shared Drive

## 🎯 Uso

### Acceso por Rol
```python
# Admin - Acceso completo
@admin_required
def gestionar_archivos():
    # Crear, leer, actualizar, eliminar

# Vendedor - Lectura y escritura
@vendedor_required  
def subir_descargar():
    # Subir y descargar archivos

# Verificador - Solo lectura
@verificador_required
def solo_ver():
    # Solo ver y descargar
```

### Navegación Segura
```python
# En lugar de exponer IDs reales
# /archivos/navigate?folder_id=1ABC123...

# Se usan rutas virtuales
# /archivos/listar?path=/carpeta1/subcarpeta
```

## 📊 Estado del Sistema

- ✅ Navegación en subcarpetas: **FUNCIONAL**
- ✅ Consulta híbrida: **APLICADA**
- ✅ Control de acceso: **IMPLEMENTADO**
- ✅ Seguridad: **CONFIGURADA**
- ✅ Interfaz de usuario: **COMPLETA**

## 🔧 Mantenimiento

### Logs de Debugging
El sistema incluye logging detallado para monitorear:
- Consultas realizadas a Google Drive API
- Resultados de consultas híbridas
- Navegación de usuarios
- Errores de acceso

### Verificación de Funcionamiento
```bash
# El sistema se verifica automáticamente en cada consulta
# Los logs mostrarán si la consulta híbrida está funcionando
```

## 📝 Notas Técnicas

1. **Shared Drive requerido**: Las cuentas de servicio no tienen cuota propia
2. **Consulta híbrida esencial**: Resuelve problemas de indexación de la API
3. **Rutas virtuales**: Mejoran la seguridad al ocultar IDs reales
4. **Control de roles**: Integrado con el sistema de autenticación existente

---

*Sistema implementado y verificado el 3 de septiembre de 2025*
