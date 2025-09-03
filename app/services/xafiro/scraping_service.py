"""
Servicio de scraping para extraer datos del registro de caja usando requests (sin navegador)
Adaptado para el proyecto Flask principal
"""
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List, Dict, Any, Optional
import logging
import time

logger = logging.getLogger(__name__)

class ScrapingService:
    @staticmethod
    def procesar_voucher_operacion(voucher_texto: str) -> tuple:
        """
        Procesa el texto del voucher y lo separa en transacción y banco
        
        Args:
            voucher_texto: Texto del voucher en formato "transaccion - banco"
            
        Returns:
            tuple: (transaccion, banco)
        """
        if not voucher_texto or voucher_texto.strip() == '':
            return None, None
        
        # Separar por el guion
        if ' - ' in voucher_texto:
            partes = voucher_texto.split(' - ', 1)  # Solo dividir en el primer guion
            transaccion = partes[0].strip() if len(partes) > 0 else None
            banco = partes[1].strip() if len(partes) > 1 else None
        elif '-' in voucher_texto:
            # Si no hay espacios alrededor del guion
            partes = voucher_texto.split('-', 1)
            transaccion = partes[0].strip() if len(partes) > 0 else None
            banco = partes[1].strip() if len(partes) > 1 else None
        else:
            # Si no hay guion, todo va a transacción
            transaccion = voucher_texto.strip()
            banco = None
        
        return transaccion, banco

    @staticmethod
    def obtener_detalle_facturacion(session: requests.Session, numero_reserva: int) -> Optional[str]:
        """
        Obtiene el detalle de la primera tabla en la página de facturación de una reserva específica
        
        Args:
            session: Sesión de requests autenticada
            numero_reserva: Número de reserva
            
        Returns:
            str: Detalle encontrado en la primera tabla o None si no se encuentra
        """
        try:
            url_facturacion = f"https://hotel.xafiro.net/caja/facturacion/{numero_reserva}"
            logger.info(f"🔍 Obteniendo detalle de facturación para reserva {numero_reserva}")
            
            # Realizar petición a la página de facturación
            response = session.get(url_facturacion, timeout=30)
            response.raise_for_status()
            
            # Parsear HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Buscar la primera tabla que contenga una columna "Detalle"
            tablas = soup.find_all('table')
            
            for i, tabla in enumerate(tablas):
                logger.debug(f"📋 Analizando tabla {i+1} de {len(tablas)}")
                
                # Buscar headers de la tabla
                headers = []
                thead = tabla.find('thead')
                if thead:
                    header_row = thead.find('tr')
                    if header_row:
                        headers = [th.get_text(strip=True) for th in header_row.find_all(['th', 'td'])]
                
                # Si no hay thead, buscar en la primera fila
                if not headers:
                    first_row = tabla.find('tr')
                    if first_row:
                        headers = [td.get_text(strip=True) for td in first_row.find_all(['th', 'td'])]
                
                logger.debug(f"📋 Headers encontrados: {headers}")
                
                # Verificar si hay una columna "Detalle"
                detalle_index = None
                for j, header in enumerate(headers):
                    if 'detalle' in header.lower():
                        detalle_index = j
                        logger.info(f"✅ Encontrada columna 'Detalle' en posición {j} de la tabla {i+1}")
                        break
                
                if detalle_index is not None:
                    detalles = []
                    # Buscar filas de datos (excluyendo header)
                    tbody = tabla.find('tbody')
                    filas = tbody.find_all('tr') if tbody else tabla.find_all('tr')[1:]  # Excluir header si no hay tbody
                    
                    # Obtener el detalle de la primera fila de datos
                    if filas:
                        primera_fila = filas[0]
                        celdas = primera_fila.find_all(['td', 'th'])
                        
                        if len(celdas) > detalle_index:
                            celda_detalle = celdas[detalle_index].get_text(strip=True)
                            
                            # Extraer texto, manejando checkboxes y otros elementos
                            texto_detalle = ""
                            
                            # Buscar elementos de texto dentro de la celda
                            elementos_texto = celda_detalle.find_all(text=True)
                            for texto in elementos_texto:
                                texto_limpio = texto.strip()
                                if texto_limpio and texto_limpio not in ['☐', '☑', '□', '✓']:
                                    texto_detalle += texto_limpio + " "
                            
                            texto_detalle = texto_detalle.strip()
                            
                            if texto_detalle:
                                detalles.append(texto_detalle)
                            
                            if celda_detalle:  # Solo retornar si no está vacío
                                detalle_completo = " | ".join(detalles)
                                logger.info(f"✅ Detalle extraído: {detalle_completo[:100]}...")
                                return detalle_completo
                
                logger.debug(f"⚠️ No se encontró columna 'Detalle' en tabla {i+1}")
            
            logger.warning(f"⚠️ No se encontró detalle en ninguna tabla para reserva {numero_reserva}")
            return None
            
        except requests.exceptions.Timeout:
            logger.error(f"⏱️ Timeout obteniendo detalle para reserva {numero_reserva}")
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"🌐 Error de conexión obteniendo detalle para reserva {numero_reserva}: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"❌ Error obteniendo detalle para reserva {numero_reserva}: {str(e)}")
            return None

    @staticmethod
    def obtener_voucher_operacion(session: requests.Session, numero_reserva: int) -> Optional[str]:
        """
        Busca el Voucher | Operación para un número de reserva específico
        Primero busca en tarjeta, luego en transferencia
        """
        urls_busqueda = [
            f"https://hotel.xafiro.net//caja/ver_popup_detalle_caja/NUL/tarjeta/3",
            f"https://hotel.xafiro.net//caja/ver_popup_detalle_caja/NUL/transferencia/3"
        ]
        
        for url in urls_busqueda:
            try:
                logger.info(f"🔍 Buscando voucher para reserva {numero_reserva} en: {url}")
                
                response = session.get(url)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Buscar tabla que contenga el número de reserva
                tabla = soup.find('table', class_=lambda x: x and 'table' in x.lower() if x else False)
                if not tabla:
                    tabla = soup.find('table')
                
                if tabla:
                    # Buscar fila que contenga el número de reserva
                    filas = tabla.find_all('tr')
                    
                    for fila in filas:
                        celdas = fila.find_all(['td', 'th'])
                        
                        # Buscar en las celdas si contiene el número de reserva
                        for i, celda in enumerate(celdas):
                            texto_celda = celda.get_text(strip=True)
                            
                            # Si encontramos el número de reserva
                            if str(numero_reserva) in texto_celda:
                                logger.info(f"✅ Encontrada reserva {numero_reserva} en {url}")
                                
                                # Buscar la columna "Voucher" o "Operación" en los encabezados
                                encabezados_fila = tabla.find('tr')
                                if encabezados_fila:
                                    encabezados = [th.get_text(strip=True) for th in encabezados_fila.find_all(['th', 'td'])]
                                    
                                    # Buscar índice de la columna Voucher/Operación
                                    voucher_index = None
                                    for idx, encabezado in enumerate(encabezados):
                                        if any(palabra in encabezado.lower() for palabra in ['voucher', 'operación', 'operacion']):
                                            voucher_index = idx
                                            break
                                    
                                    # Si encontramos la columna, extraer el valor
                                    if voucher_index is not None and voucher_index < len(celdas):
                                        voucher_value = celdas[voucher_index].get_text(strip=True)
                                        logger.info(f"📋 Voucher/Operación encontrado: {voucher_value}")
                                        return voucher_value
                                
                                # Si no hay encabezados claros, buscar en celdas adyacentes
                                # Asumir que Voucher/Operación está en las últimas columnas
                                if len(celdas) > 1:
                                    for j in range(len(celdas) - 1, max(0, len(celdas) - 4), -1):
                                        valor = celdas[j].get_text(strip=True)
                                        if valor and valor != str(numero_reserva):
                                            logger.info(f"📋 Posible Voucher/Operación: {valor}")
                                            return valor
                
            except Exception as e:
                logger.warning(f"⚠️ Error buscando en {url}: {str(e)}")
                continue
        
        logger.warning(f"❌ No se encontró Voucher/Operación para reserva {numero_reserva}")
        return None
    
    @staticmethod
    def navegar_a_registro_caja(session: requests.Session, fecha: str) -> requests.Response:
        """
        Navega al registro de caja con la fecha especificada usando requests
        """
        try:
            logger.info(f"📅 Navegando al registro de caja para fecha: {fecha}")
            
            # URL temporal - aquí se puede implementar la navegación completa
            url = "https://hotel.xafiro.net//caja/ver_popup_detalle_caja/NUL/pagos/3"
            
            response = session.get(url)
            response.raise_for_status()
            
            logger.info("✅ Página del registro de caja cargada")
            return response
            
        except Exception as e:
            logger.error(f"❌ Error navegando al registro de caja: {str(e)}")
            raise
    
    @staticmethod
    def extraer_tabla_registro_caja_html(html_content: str) -> List[Dict[str, Any]]:
        """
        Extrae los datos de la tabla del registro de caja desde HTML
        """
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Buscar la tabla
            tabla = soup.find('table', class_=lambda x: x and 'table' in x.lower() if x else False)
            
            if not tabla:
                # Buscar cualquier tabla si no encuentra con clase específica
                tabla = soup.find('table')
                
            if not tabla:
                logger.warning("❌ No se encontró ninguna tabla en el HTML")
                return []
            
            # Extraer encabezados
            thead = tabla.find('thead')
            if thead:
                encabezados = [th.get_text(strip=True) for th in thead.find_all('th')]
            else:
                # Si no hay thead, buscar la primera fila como encabezados
                primera_fila = tabla.find('tr')
                if primera_fila:
                    encabezados = [td.get_text(strip=True) for td in primera_fila.find_all(['th', 'td'])]
                else:
                    logger.warning("❌ No se pudieron extraer encabezados")
                    return []
            
            logger.info(f"📋 Encabezados encontrados: {encabezados}")
            
            # Extraer filas de datos
            tbody = tabla.find('tbody')
            if tbody:
                filas_html = tbody.find_all('tr')
            else:
                # Si no hay tbody, tomar todas las filas excepto la primera (encabezados)
                filas_html = tabla.find_all('tr')[1:]
            
            datos = []
            
            for fila in filas_html:
                celdas = fila.find_all(['td', 'th'])
                if not celdas:
                    continue
                    
                fila_datos = {}
                
                for i, celda in enumerate(celdas):
                    if i >= len(encabezados):
                        break
                        
                    valor = celda.get_text(strip=True)
                    
                    # --- Conversión según columna ---
                    if encabezados[i] == "N° Reserva":
                        try:
                            valor = int(valor) if valor else None
                        except:
                            valor = None
                    
                    elif encabezados[i].lower() in ["fecha"]:
                        try:
                            if valor:
                                # Limpiar espacios múltiples
                                valor = " ".join(valor.split())
                                fecha_original = datetime.strptime(valor, "%d-%m-%y %I:%M %p")
                                valor = fecha_original.strftime("%d/%m/%Y %H:%M")
                            else:
                                valor = None
                        except Exception as e:
                            logger.warning(f"⚠️ Error parseando fecha '{valor}': {str(e)}")
                            valor = valor  # Mantener valor original si no se puede parsear
                    
                    elif encabezados[i].lower() in ["habitación", "habitacion"]:
                        valor = str(valor) if valor else None
                    
                    elif encabezados[i].lower() == "cliente":
                        valor = str(valor) if valor else None
                    
                    elif encabezados[i].lower() == "moneda":
                        valor = str(valor) if valor else None
                    
                    elif "monto" in encabezados[i].lower():
                        try:
                            if valor:
                                # Limpiar el valor monetario
                                valor_limpio = valor.replace("S/", "").replace(",", "").replace("$", "").strip()
                                valor = float(valor_limpio) if valor_limpio else None
                            else:
                                valor = None
                        except Exception as e:
                            logger.warning(f"⚠️ Error parseando monto '{valor}': {str(e)}")
                            valor = None
                    
                    else:
                        # Para cualquier otra columna, mantener como string
                        valor = str(valor) if valor else None
                    
                    fila_datos[encabezados[i]] = valor
                
                # Solo agregar filas que tengan al menos algún dato válido
                if any(v is not None and str(v).strip() != '' for v in fila_datos.values()):
                    datos.append(fila_datos)
            
            logger.info(f"✅ Extraídos {len(datos)} registros del registro de caja")
            return datos
            
        except Exception as e:
            logger.error(f"❌ Error extrayendo la tabla: {str(e)}")
            return []
    
    @staticmethod
    def obtener_datos_completos(session: requests.Session, fecha: str) -> List[Dict[str, Any]]:
        """
        Función principal que navega y extrae todos los datos incluyendo Voucher/Operación y Detalle de facturación
        """
        try:
            # Navegar a la página principal
            response = ScrapingService.navegar_a_registro_caja(session, fecha)
            
            # Extraer datos del HTML
            html_content = response.content.decode('utf-8', errors='ignore')
            datos = ScrapingService.extraer_tabla_registro_caja_html(html_content)
            
            # Para cada registro, buscar su Voucher/Operación y Detalle
            datos_completos = []
            total_registros = len(datos)
            
            for i, registro in enumerate(datos, 1):
                # Crear copia del registro
                registro_completo = registro.copy()
                
                # Obtener número de reserva
                numero_reserva = registro.get('N° reserva')
                
                logger.info(f"🔄 Procesando registro {i}/{total_registros} - Reserva: {numero_reserva}")
                
                if numero_reserva:
                    try:
                        # Buscar Voucher/Operación
                        voucher = ScrapingService.obtener_voucher_operacion(session, numero_reserva)
                        
                        # Procesar y separar el voucher en transacción y banco
                        transaccion, banco = ScrapingService.procesar_voucher_operacion(voucher)
                        registro_completo['transaccion'] = transaccion
                        registro_completo['banco'] = banco
                        
                        # Obtener detalle de facturación
                        detalle_facturacion = ScrapingService.obtener_detalle_facturacion(session, numero_reserva)
                        registro_completo['detalle_facturacion'] = detalle_facturacion
                        
                        # Pequeña pausa para evitar sobrecargar el servidor
                        time.sleep(0.5)
                        
                    except Exception as e:
                        logger.warning(f"⚠️ Error obteniendo datos para reserva {numero_reserva}: {str(e)}")
                        registro_completo['transaccion'] = None
                        registro_completo['banco'] = None
                        registro_completo['detalle_facturacion'] = None
                else:
                    registro_completo['transaccion'] = None
                    registro_completo['banco'] = None
                    registro_completo['detalle_facturacion'] = None
                
                datos_completos.append(registro_completo)
            
            logger.info(f"✅ Datos completos obtenidos: {len(datos_completos)} registros con información de voucher y detalle")
            return datos_completos
            
        except Exception as e:
            logger.error(f"❌ Error en obtener_datos_completos: {str(e)}")
            return []
