"""
Servicio  scraping para extraer datos del registro de caja usando requests (sin navegador)
"""
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List, Dict, Any, Optional
import logging
import time

logger = logging.getLogger(__name__)

class ScrapingServiceHeadless:
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
            # Guardar HTML para debug
            with open("debug_libro_headless.html", "w", encoding="utf-8") as f:
                if 'response' in locals():
                    f.write(response.content.decode('utf-8', errors='ignore'))
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
            # Guardar HTML para debug
            with open("debug_scraping_headless.html", "w", encoding="utf-8") as f:
                f.write(html_content)
            return []
    
    @staticmethod
    def extraer_tabla_registro_caja(session: requests.Session) -> List[Dict[str, Any]]:
        """
        Extrae los datos de la tabla desde una sesión activa
        """
        # Esta función asume que ya estamos en la página correcta
        # Se puede usar para re-extraer datos de la página actual
        try:
            # Obtener la página actual
            response = session.get(session.get_response().url)  # Esto no funcionará directamente
            # Alternativa: pasar la respuesta directamente
            logger.warning("⚠️ Esta función necesita la respuesta HTML directamente")
            return []
        except Exception as e:
            logger.error(f"❌ Error en extracción: {str(e)}")
            return []
    
    @staticmethod
    def obtener_datos_completos(session: requests.Session, fecha: str) -> List[Dict[str, Any]]:
        """
        Función principal que navega y extrae todos los datos incluyendo Voucher/Operación
        """
        try:
            # Navegar a la página principal
            response = ScrapingServiceHeadless.navegar_a_registro_caja(session, fecha)
            
            # Extraer datos del HTML
            html_content = response.content.decode('utf-8', errors='ignore')
            datos = ScrapingServiceHeadless.extraer_tabla_registro_caja_html(html_content)
            
            # Para cada registro, buscar su Voucher/Operación
            datos_completos = []
            for registro in datos:
                # Crear copia del registro
                registro_completo = registro.copy()
                
                # Obtener número de reserva
                numero_reserva = registro.get('N° reserva')
                
                if numero_reserva:
                    try:
                        # Buscar Voucher/Operación
                        voucher = ScrapingServiceHeadless.obtener_voucher_operacion(session, numero_reserva)
                        
                        # Procesar y separar el voucher en transacción y banco
                        transaccion, banco = ScrapingServiceHeadless.procesar_voucher_operacion(voucher)
                        registro_completo['transaccion'] = transaccion
                        registro_completo['banco'] = banco
                        
                    except Exception as e:
                        logger.warning(f"⚠️ Error obteniendo voucher para reserva {numero_reserva}: {str(e)}")
                        registro_completo['transaccion'] = None
                        registro_completo['banco'] = None
                else:
                    registro_completo['transaccion'] = None
                    registro_completo['banco'] = None
                
                datos_completos.append(registro_completo)
            
            logger.info(f"✅ Datos completos obtenidos: {len(datos_completos)} registros con información de voucher")
            return datos_completos
            
        except Exception as e:
            logger.error(f"❌ Error en obtener_datos_completos: {str(e)}")
            return []
