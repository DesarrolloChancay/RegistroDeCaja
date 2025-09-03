"""
API REST para extracción de datos del sistema Xafiro (Modo Headless - Sin navegador)
"""
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta
from typing import Optional
import logging

# Imports locales
from models import ScrapingRequest, ScrapingResponse
from services import XafiroAuthServiceHeadless, ScrapingServiceHeadless

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Crear instancia de FastAPI
app = FastAPI(
    title="Xafiro Data Extraction API (Headless)",
    description="API para extraer datos del registro de caja del sistema Xafiro sin abrir navegador",
    version="2.0.0"
)

# Variable global para manejar el servicio de autenticación
auth_service = None

@app.on_event("startup")
async def startup_event():
    """Evento que se ejecuta al iniciar la aplicación"""
    logger.info("🚀 Iniciando Xafiro Data Extraction API (Modo Headless)")

@app.on_event("shutdown")
async def shutdown_event():
    """Evento que se ejecuta al cerrar la aplicación"""
    global auth_service
    if auth_service:
        auth_service.cerrar_sesion()
    logger.info("🛑 Cerrando Xafiro Data Extraction API (Modo Headless)")

@app.get("/")
async def root():
    """Endpoint raíz con información de la API"""
    return {
        "message": "Xafiro Data Extraction API (Headless Mode)",
        "version": "2.0.0",
        "mode": "headless",
        "description": "Extracción de datos sin navegador visible",
        "status": "active",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "mode": "headless",
        "timestamp": datetime.now().isoformat()
    }

@app.post("/extract/registro-caja", response_model=ScrapingResponse)
async def extraer_registro_caja_headless(request: ScrapingRequest = None):
    """
    Extrae datos del registro de caja para una fecha específica (MODO HEADLESS)
    
    - **fecha**: Fecha en formato YYYY-MM-DD. Si no se proporciona, usa el día anterior
    - **Sin navegador**: Utiliza requests para máxima discreción
    """
    global auth_service
    
    try:
        # Determinar fecha a consultar
        if request and request.fecha:
            try:
                fecha_obj = datetime.strptime(request.fecha, "%Y-%m-%d")
                fecha_display = fecha_obj.strftime("%Y-%m-%d")
            except ValueError:
                raise HTTPException(
                    status_code=400, 
                    detail="Formato de fecha inválido. Use YYYY-MM-DD"
                )
        else:
            fecha_obj = datetime.now() - timedelta(days=1)
            fecha_display = fecha_obj.strftime("%Y-%m-%d")

        logger.info(f"📅 Extrayendo datos para fecha: {fecha_display} (modo headless)")

        # Inicializar servicio de autenticación headless
        auth_service = XafiroAuthServiceHeadless()
        session = auth_service.iniciar_sesion()

        try:
            # Extraer datos usando requests
            datos = ScrapingServiceHeadless.obtener_datos_completos(session, fecha_display)
            
            # Preparar respuesta
            response = ScrapingResponse(
                success=True,
                message=f"Datos extraídos exitosamente para {fecha_display} (modo headless)",
                fecha_consultada=fecha_display,
                total_registros=len(datos),
                datos=datos,
                timestamp=datetime.now()
            )
            
            logger.info(f"✅ Extracción headless exitosa: {len(datos)} registros")
            return response

        finally:
            # Siempre cerrar la sesión
            auth_service.cerrar_sesion()
            auth_service = None

    except Exception as e:
        logger.error(f"❌ Error en extracción headless: {str(e)}")
        
        # Limpiar recursos en caso de error
        if auth_service:
            auth_service.cerrar_sesion()
            auth_service = None
            
        raise HTTPException(
            status_code=500,
            detail=f"Error durante la extracción headless: {str(e)}"
        )

@app.get("/extract/registro-caja/{fecha}")
async def extraer_registro_caja_fecha_headless(fecha: str):
    """
    Extrae datos del registro de caja para una fecha específica (GET) - MODO HEADLESS
    
    - **fecha**: Fecha en formato YYYY-MM-DD
    """
    request = ScrapingRequest(fecha=fecha)
    return await extraer_registro_caja_headless(request)

@app.get("/mode")
async def get_mode():
    """
    Información sobre el modo de operación
    """
    return {
        "mode": "headless",
        "description": "API funcionando sin navegador visible",
        "advantages": [
            "Más rápido",
            "Más discreto", 
            "Menos recursos",
            "Más estable"
        ],
        "timestamp": datetime.now().isoformat()
    }

@app.get("/dates/available")
async def fechas_disponibles():
    """
    Devuelve las fechas disponibles para consulta (últimos 30 días)
    """
    fechas = []
    for i in range(30):
        fecha = datetime.now() - timedelta(days=i)
        fechas.append({
            "fecha": fecha.strftime("%Y-%m-%d"),
            "fecha_display": fecha.strftime("%d/%m/%Y"),
            "dia_semana": fecha.strftime("%A")
        })
    
    return {
        "fechas_disponibles": fechas,
        "total": len(fechas),
        "mode": "headless"
    }

# Manejo global de errores
@app.exception_handler(500)
async def internal_error_handler(request, exc):
    """Manejador global de errores internos"""
    global auth_service
    if auth_service:
        auth_service.cerrar_sesion()
        auth_service = None
    
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Error interno del servidor",
            "mode": "headless",
            "timestamp": datetime.now().isoformat()
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001, reload=True)
