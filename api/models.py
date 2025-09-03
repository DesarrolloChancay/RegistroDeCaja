from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class HuespedData(BaseModel):
    """Modelo para un registro individual del registro de caja"""
    numero_reserva: Optional[int] = None
    fecha: Optional[str] = None
    habitacion: Optional[str] = None
    cliente: Optional[str] = None
    moneda: Optional[str] = None
    monto: Optional[float] = None
    transaccion: Optional[str] = None  # Parte antes del guion en Voucher/Operación
    banco: Optional[str] = None  # Parte después del guion en Voucher/Operación
    
    # Campos adicionales que puedan aparecer en la tabla
    otros_campos: Optional[dict] = {}

class ScrapingRequest(BaseModel):
    """Modelo para la solicitud de scraping"""
    fecha: Optional[str] = None  # Formato: YYYY-MM-DD, si no se proporciona usa fecha actual - 1 día
    
class ScrapingResponse(BaseModel):
    """Modelo para la respuesta del scraping"""
    success: bool
    message: str
    fecha_consultada: str
    total_registros: int
    datos: List[dict]
    timestamp: datetime

class ErrorResponse(BaseModel):
    """Modelo para respuestas de error"""
    success: bool = False
    error: str
    timestamp: datetime
