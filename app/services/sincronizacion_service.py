"""
Servicio de sincronización para importar datos desde Xafiro al sistema de registro de caja
"""
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from app.extensions import db
from app.models.registro_venta import RegistroVenta
from app.services.xafiro.auth_service import XafiroAuthService
from app.services.xafiro.scraping_service import ScrapingService
from sqlalchemy import text
from flask_login import current_user

logger = logging.getLogger(__name__)

class SincronizacionService:
    
    @staticmethod
    def obtener_mapeo_entidades():
        """
        Obtiene los mapeos de entidades de la base de datos para convertir nombres a IDs
        """
        try:
            # Obtener mapeos de empresas
            empresas_result = db.session.execute(text('SELECT id, nombre FROM empresas')).fetchall()
            empresas_map = {row.nombre.upper(): row.id for row in empresas_result}
            
            # Obtener mapeos de áreas
            areas_result = db.session.execute(text('SELECT id, nombre FROM areas')).fetchall()
            areas_map = {row.nombre.upper(): row.id for row in areas_result}
            
            # Obtener mapeos de entidades bancarias
            bancos_result = db.session.execute(text('SELECT id, nombre FROM entidades_banco')).fetchall()
            bancos_map = {row.nombre.upper(): row.id for row in bancos_result}
            
            # Obtener mapeos de medios de pago
            medios_result = db.session.execute(text('SELECT id, nombre FROM medios_pago')).fetchall()
            medios_map = {row.nombre.upper(): row.id for row in medios_result}
            
            # Obtener mapeos de centros de costo
            centros_result = db.session.execute(text('SELECT id, nombre FROM centros_costo')).fetchall()
            centros_map = {row.nombre.upper(): row.id for row in centros_result}
            
            return {
                'empresas': empresas_map,
                'areas': areas_map,
                'bancos': bancos_map,
                'medios_pago': medios_map,
                'centros_costo': centros_map
            }
        except Exception as e:
            logger.error(f"Error obteniendo mapeos de entidades: {str(e)}")
            return {
                'empresas': {},
                'areas': {},
                'bancos': {},
                'medios_pago': {},
                'centros_costo': {}
            }
    
    @staticmethod
    def mapear_medio_pago(transaccion: str) -> int:
        """
        Mapea el tipo de transacción de Xafiro a un medio de pago de la BD
        """
        if not transaccion:
            return 8  # OTROS por defecto
            
        transaccion_upper = transaccion.upper()
        
        # Mapeo de transacciones comunes
        if 'EFECTIVO' in transaccion_upper or 'CASH' in transaccion_upper:
            return 1  # EFECTIVO
        elif 'YAPE' in transaccion_upper:
            return 2  # POS - YAPE
        elif 'TARJETA' in transaccion_upper or 'CARD' in transaccion_upper or 'VISA' in transaccion_upper or 'MASTERCARD' in transaccion_upper:
            return 3  # POS - TARJETA
        elif 'PLIN' in transaccion_upper:
            return 4  # POS - PLIN
        elif 'PAGOLINK' in transaccion_upper:
            return 5  # PAGOLINK
        elif 'DEPOSITO' in transaccion_upper or 'DEPOSIT' in transaccion_upper:
            return 6  # DEPOSITO
        elif 'TRANSFERENCIA' in transaccion_upper or 'TRANSFER' in transaccion_upper:
            return 7  # TRANSFERENCIA
        else:
            return 8  # OTROS
    
    @staticmethod
    def mapear_medio_pago_mejorado(medio: str, transaccion: str) -> int:
        """
        Mapea el medio de pago combinando el campo 'Medio' y 'transaccion' de Xafiro
        """
        # Priorizar el campo 'Medio' si está disponible
        if medio:
            medio_upper = medio.upper()
            
            if 'EFECTIVO' in medio_upper or 'CASH' in medio_upper:
                return 1  # EFECTIVO
            elif 'YAPE' in medio_upper:
                return 2  # POS - YAPE
            elif 'TARJETA' in medio_upper or 'CARD' in medio_upper:
                # Si es tarjeta, verificar si es PagoLink por el número de transacción
                if transaccion and 'PAGO' in transaccion.upper():
                    return 5  # PAGOLINK
                else:
                    return 3  # POS - TARJETA
            elif 'PLIN' in medio_upper:
                return 4  # POS - PLIN
            elif 'PAGOLINK' in medio_upper or 'PAGO LINK' in medio_upper:
                return 5  # PAGOLINK
            elif 'DEPOSITO' in medio_upper or 'DEPOSIT' in medio_upper:
                return 6  # DEPOSITO
            elif 'TRANSFERENCIA' in medio_upper or 'TRANSFER' in medio_upper:
                return 7  # TRANSFERENCIA
        
        # Si no hay 'Medio' o no se encontró coincidencia, usar función original
        return SincronizacionService.mapear_medio_pago(transaccion)
    
    @staticmethod
    def mapear_entidad_banco(banco: str, mapeos: Dict) -> int:
        """
        Mapea el nombre del banco de Xafiro a un ID de entidad bancaria
        """
        if not banco:
            return 1  # BCP por defecto
            
        banco_upper = banco.upper()
        
        # Casos especiales para PagoLink
        if 'PAGO LINK' in banco_upper or 'PAGOLINK' in banco_upper:
            # Buscar PagoLink en los mapeos
            for nombre_banco, id_banco in mapeos['bancos'].items():
                if 'PAGOLINK' in nombre_banco or 'PAGO LINK' in nombre_banco:
                    return id_banco
            # Si no existe en BD, usar BCP como fallback
            return 1
        
        # Buscar coincidencias exactas primero
        if banco_upper in mapeos['bancos']:
            return mapeos['bancos'][banco_upper]
        
        # Buscar coincidencias parciales
        for nombre_banco, id_banco in mapeos['bancos'].items():
            if banco_upper in nombre_banco or nombre_banco in banco_upper:
                return id_banco
        
        # Mapeo manual de bancos comunes
        if 'BCP' in banco_upper or 'CREDITO' in banco_upper:
            return 1  # BCP
        elif 'BBVA' in banco_upper or 'CONTINENTAL' in banco_upper:
            return 2  # BBVA
        elif 'SCOTIA' in banco_upper:
            return 3  # Scotiabank
        elif 'INTER' in banco_upper:
            return 4  # Interbank
        
        return 1  # BCP por defecto
    
    @staticmethod
    def convertir_fecha_xafiro(fecha_str: str) -> Optional[datetime]:
        """
        Convierte una fecha de formato Xafiro a datetime
        """
        if not fecha_str:
            return None
            
        try:
            # Formato esperado: "dd/mm/yyyy HH:MM"
            if '/' in fecha_str and ' ' in fecha_str:
                return datetime.strptime(fecha_str, "%d/%m/%Y %H:%M")
            elif '/' in fecha_str:
                return datetime.strptime(fecha_str, "%d/%m/%Y")
            else:
                # Intentar otros formatos comunes
                for formato in ["%Y-%m-%d %H:%M", "%Y-%m-%d", "%d-%m-%Y %H:%M", "%d-%m-%Y"]:
                    try:
                        return datetime.strptime(fecha_str, formato)
                    except:
                        continue
                        
        except Exception as e:
            logger.warning(f"Error convirtiendo fecha '{fecha_str}': {str(e)}")
            
        return None
    
    @staticmethod
    def generar_id_xafiro_unico(numero_reserva: int, fecha: datetime) -> str:
        """
        Genera un ID único de Xafiro basado en la reserva y fecha
        """
        if fecha:
            fecha_str = fecha.strftime("%Y%m%d")
            return f"XAF{numero_reserva:06d}-{fecha_str}"
        else:
            fecha_str = datetime.now().strftime("%Y%m%d")
            return f"XAF{numero_reserva:06d}-{fecha_str}"
    
    @staticmethod
    def mapear_registro_xafiro_a_bd(registro_xafiro: Dict, mapeos: Dict) -> Dict:
        """
        Mapea un registro de Xafiro a la estructura de la base de datos
        """
        try:
            # Extraer datos del registro de Xafiro con los nombres correctos
            numero_reserva = registro_xafiro.get('N° reserva') or registro_xafiro.get('numero_reserva')
            fecha_str = registro_xafiro.get('Fecha') or registro_xafiro.get('fecha')
            habitacion = registro_xafiro.get('Habitación') or registro_xafiro.get('habitacion')
            cliente = registro_xafiro.get('Cliente') or registro_xafiro.get('cliente')
            monto = registro_xafiro.get('Monto') or registro_xafiro.get('monto')
            medio = registro_xafiro.get('Medio') or registro_xafiro.get('medio')
            modo = registro_xafiro.get('Modo') or registro_xafiro.get('modo')
            moneda = registro_xafiro.get('Moneda') or registro_xafiro.get('moneda')
            transaccion = registro_xafiro.get('transaccion')
            banco = registro_xafiro.get('banco')
            detalle_facturacion = registro_xafiro.get('detalle_facturacion')  # Nuevo campo
            
            # Validar datos mínimos requeridos
            if not numero_reserva:
                logger.warning(f"Registro sin número de reserva: {registro_xafiro}")
                return None
                
            if not fecha_str:
                logger.warning(f"Registro sin fecha: {registro_xafiro}")
                return None
                
            if not monto:
                logger.warning(f"Registro sin monto: {registro_xafiro}")
                return None
            
            if not transaccion:
                logger.warning(f"Registro sin número de transacción: {registro_xafiro}")
                return None
            
            # Convertir numero_reserva a entero si es string
            try:
                numero_reserva = int(numero_reserva)
            except (ValueError, TypeError):
                logger.warning(f"Número de reserva inválido: {numero_reserva}")
                return None
            
            # Convertir fecha
            fecha_obj = SincronizacionService.convertir_fecha_xafiro(fecha_str)
            if not fecha_obj:
                logger.warning(f"No se pudo convertir fecha: {fecha_str}")
                return None
                
            fecha_registro = fecha_obj.date()
            
            # Generar ID único de Xafiro (ej: XAF004460-20250902)
            id_xafiro = SincronizacionService.generar_id_xafiro_unico(numero_reserva, fecha_obj)
            
            # El recibo debe ser el número de transacción real de Xafiro
            recibo = str(transaccion)
            
            # Mapear medio de pago basado en el campo 'Medio' y 'transaccion'
            medio_pago_id = SincronizacionService.mapear_medio_pago_mejorado(medio, transaccion)
            
            # Mapear entidad bancaria
            entidad_banco_id = SincronizacionService.mapear_entidad_banco(banco, mapeos)
            
            # Determinar área y centro de costo (por defecto HOTEL)
            area_id = mapeos['areas'].get('HOTEL', 1)
            centro_costo_id = mapeos['centros_costo'].get('CAJA - HOTEL', 
                                                       mapeos['centros_costo'].get('Caja - Hotel', 1))
            
            # Empresa por defecto
            empresa_id = mapeos['empresas'].get('RESORT', 1)
            
            # Construir detalle: priorizar el detalle de facturación
            if detalle_facturacion and detalle_facturacion.strip():
                # Usar el detalle de facturación obtenido desde Xafiro
                detalle = detalle_facturacion.strip()
                logger.info(f"✅ Usando detalle de facturación: '{detalle}' para reserva {numero_reserva}")
            else:
                # Fallback: construir detalle con información disponible
                detalle_partes = []
                if cliente:
                    detalle_partes.append(f"Cliente: {cliente}")
                if habitacion:
                    detalle_partes.append(f"Habitación: {habitacion}")
                if numero_reserva:
                    detalle_partes.append(f"Reserva: {numero_reserva}")
                if moneda and moneda != 'PEN':
                    detalle_partes.append(f"Moneda: {moneda}")
                    
                detalle = " | ".join(detalle_partes) if detalle_partes else "Registro importado desde Xafiro"
                logger.info(f"⚠️ Usando detalle construido: '{detalle}' para reserva {numero_reserva}")
            
            # Convertir monto a float
            try:
                monto_float = float(monto)
            except (ValueError, TypeError):
                logger.warning(f"Monto inválido: {monto}")
                monto_float = 0.0
            
            # Retornar datos mapeados
            return {
                'id_xafiro': id_xafiro,  # ID único generado
                'recibo': recibo,        # Número de transacción real
                'medio_pago_id': medio_pago_id,
                'entidad_banco_id': entidad_banco_id,
                'area_id': area_id,
                'centro_costo_id': centro_costo_id,
                'detalle': detalle,
                'empresa_id': empresa_id,
                'monto': monto_float,
                'confirmado': False,
                'fecha_registro_pago': fecha_registro,
                'fecha_comprobante': fecha_obj,
                'confirmado_redes': False
            }
            
        except Exception as e:
            logger.error(f"Error mapeando registro de Xafiro: {str(e)}")
            logger.error(f"Registro problemático: {registro_xafiro}")
            return None
    
    @staticmethod
    def sincronizar_registros(fecha: str = None) -> Dict[str, Any]:
        """
        Función principal de sincronización que extrae datos de Xafiro e inserta en BD
        """
        try:
            # Determinar fecha a sincronizar
            if not fecha:
                fecha_obj = datetime.now() - timedelta(days=1)
                fecha = fecha_obj.strftime("%Y-%m-%d")
            
            logger.info(f"🔄 Iniciando sincronización para fecha: {fecha}")
            
            # 1. Inicializar servicios de Xafiro
            auth_service = XafiroAuthService()
            session = auth_service.iniciar_sesion()
            
            try:
                # 2. Extraer datos de Xafiro
                datos_xafiro = ScrapingService.obtener_datos_completos(session, fecha)
                
                if not datos_xafiro:
                    return {
                        'success': False,
                        'message': 'No se encontraron datos en Xafiro para la fecha especificada',
                        'total_extraidos': 0,
                        'total_insertados': 0,
                        'errores': []
                    }
                
                # 3. Obtener mapeos de la base de datos
                mapeos = SincronizacionService.obtener_mapeo_entidades()
                
                # 4. Procesar e insertar registros
                registros_insertados = 0
                errores = []
                
                for registro_xafiro in datos_xafiro:
                    try:
                        logger.info(f"🔍 Procesando registro: {registro_xafiro}")
                        
                        # Mapear registro de Xafiro a estructura de BD
                        registro_bd = SincronizacionService.mapear_registro_xafiro_a_bd(registro_xafiro, mapeos)
                        
                        if not registro_bd:
                            error_msg = f"Error mapeando registro: {registro_xafiro}"
                            errores.append(error_msg)
                            logger.warning(error_msg)
                            continue
                        
                        logger.info(f"✅ Registro mapeado correctamente: {registro_bd['recibo']}")
                        
                        # Verificar si ya existe el registro (por recibo o id_xafiro)
                        registro_existente = None
                        if registro_bd['id_xafiro']:
                            registro_existente = db.session.execute(
                                text('SELECT id FROM registros_ventas WHERE recibo = :recibo OR id_xafiro = :id_xafiro'),
                                {'recibo': registro_bd['recibo'], 'id_xafiro': registro_bd['id_xafiro']}
                            ).fetchone()
                        else:
                            registro_existente = db.session.execute(
                                text('SELECT id FROM registros_ventas WHERE recibo = :recibo'),
                                {'recibo': registro_bd['recibo']}
                            ).fetchone()
                        
                        if registro_existente:
                            logger.info(f"📋 Registro ya existe: {registro_bd['recibo']}")
                            continue
                        
                        # Insertar nuevo registro
                        insert_query = text('''
                            INSERT INTO registros_ventas (
                                id_xafiro, recibo, medio_pago_id, entidad_banco_id, area_id, 
                                centro_costo_id, detalle, empresa_id, monto, confirmado, 
                                fecha_registro_pago, fecha_comprobante, confirmado_redes
                            ) VALUES (
                                :id_xafiro, :recibo, :medio_pago_id, :entidad_banco_id, :area_id,
                                :centro_costo_id, :detalle, :empresa_id, :monto, :confirmado,
                                :fecha_registro_pago, :fecha_comprobante, :confirmado_redes
                            )
                        ''')
                        
                        db.session.execute(insert_query, registro_bd)
                        registros_insertados += 1
                        
                    except Exception as e:
                        error_msg = f"Error insertando registro {registro_xafiro}: {str(e)}"
                        errores.append(error_msg)
                        logger.error(error_msg)
                
                # 5. Confirmar transacción
                db.session.commit()
                
                resultado = {
                    'success': True,
                    'message': f'Sincronización completada. {registros_insertados} registros insertados.',
                    'total_extraidos': len(datos_xafiro),
                    'total_insertados': registros_insertados,
                    'errores': errores,
                    'fecha_sincronizada': fecha
                }
                
                logger.info(f"✅ {resultado['message']}")
                return resultado
                
            finally:
                # Cerrar sesión de Xafiro
                auth_service.cerrar_sesion()
                
        except Exception as e:
            db.session.rollback()
            error_msg = f"Error en sincronización: {str(e)}"
            logger.error(error_msg)
            
            return {
                'success': False,
                'message': error_msg,
                'total_extraidos': 0,
                'total_insertados': 0,
                'errores': [error_msg]
            }
