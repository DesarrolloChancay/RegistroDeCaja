"""
Servicio de autenticación para Xafiro usando requests (sin navegador)
"""
import requests
from bs4 import BeautifulSoup
import time
import os
from typing import Optional, Dict
import logging
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

logger = logging.getLogger(__name__)

class XafiroAuthServiceHeadless:
    def __init__(self):
        self.session = requests.Session()
        # Headers actualizados según los requerimientos de Xafiro
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'sec-ch-ua': '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        })
        
    def iniciar_sesion(self, empresa: str = None, 
                      usuario: str = None, 
                      password: str = None) -> requests.Session:
        """
        Realiza el login usando requests sin abrir navegador
        Las credenciales se toman del archivo .env si no se proporcionan
        """
        try:
            # Usar credenciales del .env si no se proporcionan
            empresa = empresa or os.getenv("XAFIRO_EMPRESA")
            usuario = usuario or os.getenv("XAFIRO_USUARIO")
            password = password or os.getenv("XAFIRO_PASSWORD")
            
            logger.info("🔐 Iniciando sesión en Xafiro (modo headless)")
            
            # Paso 1: Obtener la página de login
            login_url = "https://hotel.xafiro.net/acceso"
            response = self.session.get(login_url)
            response.raise_for_status()
            
            logger.info(f"📄 Página de login obtenida: {response.status_code}")
            
            # Paso 2: Parsear el formulario para obtener tokens CSRF si los hay
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Buscar campos ocultos (tokens CSRF, etc.)
            hidden_inputs = {}
            for hidden_input in soup.find_all('input', type='hidden'):
                name = hidden_input.get('name')
                value = hidden_input.get('value')
                if name and value:
                    hidden_inputs[name] = value
                    logger.info(f"🔑 Campo oculto encontrado: {name} = {value}")
            
            # Paso 3: Preparar headers específicos para el POST
            login_headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Origin': 'https://hotel.xafiro.net',
                'Referer': 'https://hotel.xafiro.net/acceso',
                'sec-ch-ua': '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36'
            }
            
            # Paso 4: Preparar datos del login (CORREGIDO: 'pass' en lugar de 'password')
            login_data = {
                'empresa': empresa,
                'usuario': usuario,
                'pass': password,  # ¡CORRECCIÓN! El campo se llama 'pass' no 'password'
                'enviar': 'Ingresar',  # Botón de submit
                **hidden_inputs  # Incluir cualquier campo oculto
            }
            
            logger.info(f"📤 Enviando datos de login: empresa={empresa}, usuario={usuario}")
            
            # Paso 5: Realizar el login con headers específicos
            login_response = self.session.post(
                login_url, 
                data=login_data,
                headers=login_headers,
                allow_redirects=True
            )
            login_response.raise_for_status()
            
            logger.info(f"📥 Respuesta del login: {login_response.status_code}, URL: {login_response.url}")
            
            # Paso 6: Verificar si el login fue exitoso
            if self._verificar_login_exitoso(login_response):
                logger.info("✅ Login exitoso en Xafiro")
                return self.session
            else:
                logger.error("❌ Login fallido - verificando respuesta")
                # Guardar HTML de respuesta para debug
                with open("debug_login_response.html", "w", encoding="utf-8") as f:
                    f.write(login_response.content.decode('utf-8', errors='ignore'))
                raise Exception("Login fallido - revisar credenciales o debug_login_response.html")
                
        except Exception as e:
            logger.error(f"❌ Error durante el login: {str(e)}")
            # Guardar HTML para debug
            if 'response' in locals():
                with open("debug_login_error.html", "w", encoding="utf-8") as f:
                    f.write(response.content.decode('utf-8', errors='ignore'))
            raise Exception(f"Error en el login: {str(e)}")
    
    def _verificar_login_exitoso(self, response: requests.Response) -> bool:
        """
        Verifica si el login fue exitoso analizando la respuesta
        """
        logger.info(f"🔍 Verificando login - URL: {response.url}")
        
        # 1. Verificar redirección exitosa - si seguimos en /acceso es malo
        if response.url.endswith('/acceso') or '/acceso' in response.url:
            logger.warning("⚠️ Aún en página de acceso - posible fallo de login")
            return False
        
        # 2. Verificar status code
        if response.status_code != 200:
            logger.warning(f"⚠️ Status code inesperado: {response.status_code}")
            return False
            
        # 3. Buscar elementos que indiquen sesión iniciada
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Buscar indicadores comunes de dashboard/home
        indicadores_exitosos = [
            soup.find('a', string=lambda text: text and 'salir' in text.lower()),
            soup.find('a', string=lambda text: text and 'logout' in text.lower()),
            soup.find('a', string=lambda text: text and 'cerrar sesión' in text.lower()),
            soup.find('span', string=lambda text: text and ('bienvenido' in text.lower() or 'welcome' in text.lower())),
            soup.find('div', {'class': lambda x: x and ('dashboard' in x.lower() or 'menu' in x.lower() or 'navbar' in x.lower()) if x else False}),
            soup.find('nav'),
            soup.find('ul', {'class': lambda x: x and 'menu' in x.lower() if x else False}),
        ]
        
        # 4. Verificar cookies de sesión
        cookies_sesion = [name for name in self.session.cookies.keys() 
                         if any(keyword in name.lower() for keyword in ['session', 'auth', 'login', 'token', 'xafiro'])]
        
        logger.info(f"🍪 Cookies encontradas: {list(self.session.cookies.keys())}")
        logger.info(f"🍪 Cookies de sesión: {cookies_sesion}")
        
        # 5. Buscar indicadores de error en el contenido
        texto_respuesta = response.text.lower()
        errores_comunes = [
            'error en el usuario o contraseña',
            'usuario o contraseña incorrectos',
            'credenciales inválidas',
            'error de autenticación',
            'login failed',
            'invalid credentials'
        ]
        
        tiene_errores = any(error in texto_respuesta for error in errores_comunes)
        if tiene_errores:
            logger.error("❌ Encontrado mensaje de error específico en la respuesta")
            # Extraer el mensaje de error específico
            soup_text = soup.get_text()
            if 'error en el usuario o contraseña' in soup_text.lower():
                logger.error("🔑 Error específico: Credenciales incorrectas")
            return False
        
        # Si cualquier indicador es positivo, consideramos login exitoso
        indicadores_encontrados = [i for i in indicadores_exitosos if i is not None]
        login_exitoso = len(indicadores_encontrados) > 0 or len(cookies_sesion) > 0
        
        logger.info(f"🔍 Indicadores encontrados: {len(indicadores_encontrados)}")
        logger.info(f"🔍 Cookies de sesión: {len(cookies_sesion)}")
        logger.info(f"🔍 Login exitoso: {login_exitoso}")
        
        if not login_exitoso:
            # Guardar debug si el login falla
            with open("debug_login_verificacion.html", "w", encoding="utf-8") as f:
                f.write(response.content.decode('utf-8', errors='ignore'))
            logger.error("❌ Login no verificado - revisar debug_login_verificacion.html")
                
        return login_exitoso
    
    def navegar_a_url(self, url: str) -> requests.Response:
        """
        Navega a una URL específica manteniendo la sesión
        """
        try:
            response = self.session.get(url)
            response.raise_for_status()
            logger.info(f"✅ Navegación exitosa a: {url}")
            return response
        except Exception as e:
            logger.error(f"❌ Error navegando a {url}: {str(e)}")
            raise
    
    def cerrar_sesion(self):
        """
        Cierra la sesión
        """
        try:
            # Intentar hacer logout si existe la URL
            logout_urls = [
                "https://hotel.xafiro.net/logout",
                "https://hotel.xafiro.net/salir",
                "https://hotel.xafiro.net/acceso/logout"
            ]
            
            for logout_url in logout_urls:
                try:
                    self.session.get(logout_url, timeout=5)
                    break
                except:
                    continue
                    
        except Exception as e:
            logger.warning(f"⚠️ No se pudo hacer logout formal: {str(e)}")
        finally:
            # Limpiar sesión
            self.session.close()
            logger.info("🔐 Sesión cerrada")
    
    def get_session(self) -> requests.Session:
        """
        Devuelve la sesión actual
        """
        return self.session