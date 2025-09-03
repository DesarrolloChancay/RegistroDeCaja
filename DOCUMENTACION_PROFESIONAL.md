# SISTEMA DE REGISTRO DE CAJA - DOCUMENTACIÓN TÉCNICA PROFESIONAL

**Versión 1.0 | Agosto 2025**

---

## PÁGINA DE INTRODUCCIÓN

### Información del Proyecto

**Nombre del Sistema**: Sistema de Registro de Caja  
**Organización**: Castillo de Chancay  
**Versión**: 1.0  
**Fecha de Elaboración**: Agosto 2025  
**Estado**: Producción  

### Información del Documento

**Tipo de Documento**: Documentación Técnica Profesional  
**Clasificación**: Confidencial - Uso Interno  
**Idioma**: Español  
**Formato**: Markdown  
**Páginas**: Documento Digital Extenso  

### Equipo de Desarrollo

**Desarrollador Principal**: Equipo de Desarrollo Chancay  
**Arquitecto de Software**: Equipo Técnico  
**Administrador de Base de Datos**: Especialista BD  
**Responsable de Calidad**: Control de Calidad  
**Documentación Técnica**: Analista de Sistemas  

### Resumen Ejecutivo

El presente documento constituye la documentación técnica completa del **Sistema de Registro de Caja** desarrollado para el Castillo de Chancay. Este sistema web, construido sobre tecnología Flask (Python), tiene como objetivo principal centralizar y automatizar la gestión de registros financieros, implementando un robusto sistema de confirmación multinivel y auditoría completa.

### Propósito del Documento

Esta documentación técnica ha sido elaborada para:

- **Desarrolladores**: Proporcionar especificaciones técnicas detalladas para mantenimiento y futuras mejoras
- **Administradores de Sistema**: Ofrecer guías completas de instalación, configuración y operación
- **Usuarios Finales**: Facilitar manuales de uso específicos según roles y responsabilidades
- **Auditores**: Documentar controles internos y procedimientos de seguridad implementados
- **Directivos**: Presentar una visión integral del sistema y sus beneficios organizacionales

### Alcance del Sistema

El Sistema de Registro de Caja abarca:

**Funcionalidades Principales**:
- Gestión centralizada de registros de transacciones
- Sistema de confirmación por roles (Redes y Gerencia)
- Confirmación individual y masiva de registros
- Auditoría automática de todas las operaciones
- Exportación de datos para análisis financiero
- Control granular de acceso por usuarios

**Beneficios Organizacionales**:
- Mejora en la transparencia de operaciones financieras
- Reducción significativa de errores manuales
- Cumplimiento de estándares de auditoría interna
- Optimización de tiempos de procesamiento
- Generación automática de reportes ejecutivos

### Estructura del Documento

La documentación está organizada en 11 secciones principales:

1. **Análisis del Problema**: Identificación de necesidades y justificación
2. **Especificaciones Técnicas**: Requisitos funcionales y no funcionales
3. **Casos de Uso**: Interacciones detalladas por tipo de usuario
4. **Arquitectura del Sistema**: Diseño técnico y componentes
5. **Prototipado**: Wireframes e interfaz de usuario
6. **Plan de Pruebas**: Estrategias de testing y validación
7. **Configuración de Base de Datos**: Instalación y mantenimiento de BD
8. **Configuración Técnica**: Despliegue y administración del sistema
9. **Manual de Usuario**: Guías operativas por rol
10. **Anexos**: Información complementaria y recursos adicionales

### Audiencia Objetivo

**Nivel Técnico**:
- Desarrolladores de software con experiencia en Python/Flask
- Administradores de sistemas Linux/Windows
- Especialistas en bases de datos MySQL
- Profesionales de seguridad informática

**Nivel Operativo**:
- Personal administrativo del Castillo de Chancay
- Supervisores de área y gerencia
- Personal de contabilidad y finanzas
- Auditores internos y externos

**Nivel Ejecutivo**:
- Directores y gerentes generales
- Responsables de tecnología
- Personal de control interno

### Convenciones del Documento

**Formato de Código**:
```
Los bloques de código aparecen en este formato
```

**Elementos de Interfaz**: Los elementos clickeables aparecen entre `corchetes`

**Rutas de Archivo**: `/ruta/completa/al/archivo`

**Variables de Entorno**: `VARIABLE_ENTORNO`

**Comandos de Terminal**: 
```bash
comando a ejecutar
```

**Notas Importantes**:
> Las notas importantes aparecen en este formato

**Advertencias**:
⚠️ Las advertencias aparecen con este símbolo

### Política de Confidencialidad

Este documento contiene información confidencial y de propiedad exclusiva del Castillo de Chancay. Su distribución está restringida al personal autorizado y no debe ser compartido con terceros sin autorización expresa. El uso indebido de esta información está sujeto a las políticas internas de seguridad de la información.

### Control de Versiones

| Versión | Fecha | Autor | Descripción |
|---------|--------|-------|-------------|
| 1.0 | Agosto 2025 | Equipo Desarrollo | Versión inicial completa |

### Contacto y Soporte

Para consultas técnicas o aclaraciones sobre este documento:

**Equipo de Desarrollo**: desarrollo@castillodechancay.pe  

---

*Este documento ha sido generado automáticamente y revisado por el equipo técnico. Para la versión más actualizada, consulte el repositorio oficial del proyecto.*

---

## TABLA DE CONTENIDOS

1. [Planteamiento del Problema](#1-planteamiento-del-problema)
2. [Especificación de Requisitos](#2-especificación-de-requisitos)
3. [Casos de Uso del Sistema](#3-casos-de-uso-del-sistema)
4. [Informe General del Sistema](#4-informe-general-del-sistema)
5. [Arquitectura y Diseño](#5-arquitectura-y-diseño)
6. [Prototipado del Sistema](#6-prototipado-del-sistema)
7. [Plan de Pruebas](#7-plan-de-pruebas)
8. [Manual de Configuración BD](#8-manual-de-configuración-bd)
9. [Manual Técnico de Configuración](#9-manual-técnico-de-configuración)
10. [Manual de Usuario](#10-manual-de-usuario)
11. [Anexos](#11-anexos)

---

## 1. PLANTEAMIENTO DEL PROBLEMA

### 1.1 Contexto del Problema

El Castillo de Chancay requiere un sistema centralizado para la gestión y auditoría de registros de caja que permita:

- **Control de transacciones**: Seguimiento detallado de todas las operaciones financieras
- **Verificación multinivel**: Confirmación por diferentes áreas (Redes y Gerencia)
- **Auditoría completa**: Registro histórico de cambios y responsables
- **Gestión de usuarios**: Control de acceso basado en roles específicos
- **Exportación de datos**: Generación de reportes para análisis financiero

### 1.2 Problemática Identificada

1. **Falta de trazabilidad**: Sin seguimiento claro de quién y cuándo confirma las transacciones
2. **Procesos manuales**: Confirmaciones realizadas sin validación automática
3. **Ausencia de auditoría**: No hay registro de cambios realizados en los datos
4. **Control de acceso deficiente**: Sin restricciones claras por roles de usuario
5. **Reportería limitada**: Dificultad para generar informes consolidados

### 1.3 Justificación

La implementación de este sistema permitirá:
- Mejorar la transparencia en las operaciones financieras
- Reducir errores humanos mediante validaciones automáticas
- Cumplir con estándares de auditoría y control interno
- Optimizar tiempos de procesamiento
- Generar reportes precisos para toma de decisiones

---

## 2. ESPECIFICACIÓN DE REQUISITOS

### 2.1 Requisitos Funcionales

#### RF001 - Autenticación y Autorización
- **Descripción**: El sistema debe permitir login seguro con roles diferenciados
- **Prioridad**: Alta
- **Roles**: Admin, Verificador, Vendedor, Contabilidad

#### RF002 - Gestión de Registros
- **Descripción**: CRUD completo de registros de caja con validaciones
- **Prioridad**: Alta
- **Funciones**: Crear, leer, actualizar, eliminar registros

#### RF003 - Confirmación Individual
- **Descripción**: Confirmar registros uno por uno con fecha y hora
- **Prioridad**: Alta
- **Validaciones**: Fecha obligatoria, usuario autorizado

#### RF004 - Confirmación Masiva
- **Descripción**: Confirmar múltiples registros simultáneamente
- **Prioridad**: Media
- **Restricciones**: Solo registros con fecha completa

#### RF005 - Sistema de Auditoría
- **Descripción**: Registro automático de todos los cambios
- **Prioridad**: Alta
- **Información**: Usuario, fecha, IP, motivo, valores anterior/nuevo

#### RF006 - Exportación de Datos
- **Descripción**: Generar reportes en Excel
- **Prioridad**: Media
- **Formatos**: XLSX con formato específico

#### RF007 - Filtros y Búsqueda
- **Descripción**: Filtrar registros por múltiples criterios
- **Prioridad**: Media
- **Criterios**: Fecha, estado, usuario, empresa

### 2.2 Requisitos No Funcionales

#### RNF001 - Rendimiento
**¿Con qué rapidez devuelve resultados el sistema?**
- **Tiempo de respuesta**: Máximo 3 segundos para consultas estándar
- **Tiempo de carga inicial**: Máximo 5 segundos para login y dashboard
- **Consultas complejas**: Máximo 8 segundos para reportes extensos
- **Operaciones CRUD**: Máximo 2 segundos para crear/actualizar registros
- **Confirmación individual**: Máximo 1 segundo de procesamiento
- **Confirmación masiva**: Máximo 30 segundos para 100 registros
- **Exportación Excel**: Máximo 15 segundos para 1000 registros
- **Concurrencia**: Soporte para 50 usuarios simultáneos
- **Paginación**: Máximo 50 registros por página para optimizar carga

#### RNF002 - Escalabilidad
**¿Cuánto cambiará el rendimiento con cargas de trabajo mayores?**
- **Crecimiento de usuarios**: Degradación máxima del 20% con 100 usuarios simultáneos
- **Volumen de datos**: Mantener rendimiento con hasta 100,000 registros
- **Escalabilidad horizontal**: Arquitectura preparada para múltiples instancias
- **Base de datos**: Soporte para particionado de tablas por fecha
- **Memoria**: Uso máximo de 4GB RAM en pico de carga
- **CPU**: Uso máximo del 80% en operaciones intensivas
- **Almacenamiento**: Crecimiento estimado de 1GB por año
- **Red**: Ancho de banda mínimo de 10 Mbps por servidor

#### RNF003 - Portabilidad
**¿En qué hardware, sistemas operativos y navegadores se ejecuta el software?**

**Sistemas Operativos del Servidor:**
- **Linux**: Ubuntu 20.04+, CentOS 8+, Debian 11+
- **Windows**: Windows Server 2019+, Windows 10+
- **Contenedores**: Docker 20.10+, Kubernetes 1.20+

**Navegadores Web Soportados:**
- **Chrome**: Versión 90+ (Recomendado)
- **Firefox**: Versión 88+
- **Safari**: Versión 14+ (macOS/iOS)
- **Edge**: Versión 90+
- **Mobile**: Chrome Mobile, Safari Mobile

**Requisitos de Hardware Mínimos:**
- **Servidor**: 2 CPU cores, 2GB RAM, 10GB almacenamiento
- **Cliente**: Cualquier dispositivo con navegador web moderno
- **Red**: Conexión a internet de 1 Mbps mínimo

**Tecnologías Base:**
- **Python**: 3.10+
- **MySQL**: 8.0+
- **Flask**: 3.0+
- **JavaScript**: ES6+ compatible

#### RNF004 - Compatibilidad
**¿El sistema entra en conflicto con otras aplicaciones y procesos?**
- **Puertos**: Configurable, por defecto 5000 (no conflicto con servicios estándar)
- **Base de datos**: MySQL independiente, sin interferencia con otras aplicaciones
- **Archivos**: Estructura de directorios aislada en `/opt/registro_caja/`
- **Servicios**: Compatible con Apache/Nginx como proxy reverso
- **Antivirus**: Whitelist de archivos `.py` y directorio de aplicación
- **Firewall**: Configuración específica para puertos necesarios
- **SSL/TLS**: Compatible con certificados Let's Encrypt y comerciales
- **Integración**: APIs REST para futuras integraciones con sistemas existentes

#### RNF005 - Fiabilidad
**¿Con qué frecuencia experimenta el sistema fallos críticos?**
- **MTBF (Mean Time Between Failures)**: Mínimo 720 horas (30 días)
- **Tasa de errores**: Máximo 0.1% de transacciones fallidas
- **Recuperación automática**: Reinicio automático ante fallos no críticos
- **Tolerancia a fallos**: Degradación gradual ante sobrecarga
- **Validación de datos**: 100% de transacciones validadas antes de confirmar
- **Transacciones atómicas**: Rollback automático en caso de error
- **Logs de error**: Registro completo para análisis post-fallo
- **Monitoreo**: Alertas automáticas ante comportamiento anómalo

#### RNF006 - Mantenibilidad
**¿Cuánto tiempo se tarda en solucionar problemas cuando surgen?**
- **Diagnóstico**: Máximo 15 minutos para identificar problemas
- **Corrección menor**: Máximo 2 horas para bugs no críticos
- **Corrección crítica**: Máximo 4 horas para fallos que afectan operación
- **Despliegue**: Máximo 30 minutos para actualizaciones menores
- **Documentación**: 100% de código documentado para facilitar mantenimiento
- **Logs detallados**: Trazabilidad completa para debugging
- **Ambiente de pruebas**: Réplica exacta para testing antes de producción
- **Backup/Restore**: Procedimientos de recuperación en máximo 1 hora

#### RNF007 - Disponibilidad
**¿Cuál es la duración promedio del tiempo de inactividad del sistema?**
- **Uptime objetivo**: 99.5% de disponibilidad (3.6 horas/mes de downtime)
- **Ventana de mantenimiento**: Domingos 2:00-4:00 AM programado
- **Backup automático**: Diario a las 3:00 AM sin afectar operación
- **Recuperación rápida**: RTO (Recovery Time Objective) de 4 horas máximo
- **RPO (Recovery Point Objective)**: Pérdida máxima de 1 hora de datos
- **Monitoreo 24/7**: Verificación automática cada 5 minutos
- **Alertas tempranas**: Notificación inmediata ante degradación
- **Plan de contingencia**: Procedimientos documentados para emergencias

#### RNF008 - Seguridad
**¿Qué tan bien están protegidos el sistema y sus datos contra ataques?**

**Autenticación y Autorización:**
- **Contraseñas**: Hash bcrypt con salt, mínimo 8 caracteres
- **Sesiones**: Timeout automático después de 30 minutos de inactividad
- **Tokens**: JWT con expiración y rotación automática
- **Roles**: Control granular de permisos por funcionalidad

**Protección de Datos:**
- **Cifrado en tránsito**: TLS 1.3 para todas las comunicaciones
- **Cifrado en reposo**: Datos sensibles cifrados en base de datos
- **Sanitización**: Validación y escape de todos los inputs
- **SQL Injection**: Uso exclusivo de consultas parametrizadas

**Protección contra Ataques:**
- **CSRF**: Tokens de protección en formularios
- **XSS**: Sanitización y escape de outputs
- **Brute Force**: Bloqueo temporal tras 5 intentos fallidos
- **Rate Limiting**: Máximo 100 requests por minuto por IP

**Auditoría y Compliance:**
- **Logs de acceso**: Registro completo de todas las acciones
- **Trazabilidad**: IP, usuario, fecha/hora en cada operación
- **Backup seguro**: Cifrado de respaldos con claves rotativas
- **Cumplimiento**: Alineado con mejores prácticas de seguridad

#### RNF009 - Usabilidad
**¿Qué tan fácil es usar el sistema?**

**Interfaz de Usuario:**
- **Diseño intuitivo**: Navegación clara y consistente
- **Responsive**: Adaptación automática a móviles y tablets
- **Carga rápida**: Interfaz optimizada para conexiones lentas
- **Accesibilidad**: Cumplimiento con estándares WCAG 2.1 AA

**Experiencia de Usuario:**
- **Feedback inmediato**: Confirmaciones visuales de todas las acciones
- **Mensajes claros**: Errores y éxitos en lenguaje natural
- **Curva de aprendizaje**: Máximo 2 horas de capacitación por rol
- **Ayuda contextual**: Tooltips y guías integradas

**Productividad:**
- **Confirmación masiva**: Procesamiento de múltiples registros simultáneamente
- **Filtros avanzados**: Búsqueda rápida por múltiples criterios
- **Exportación sencilla**: Un clic para generar reportes
- **Shortcuts**: Atajos de teclado para operaciones frecuentes

**Soporte Multi-dispositivo:**
- **Desktop**: Funcionalidad completa en resoluciones 1366x768+
- **Tablet**: Interfaz optimizada para pantallas táctiles
- **Móvil**: Funciones esenciales disponibles en smartphones
- **Offline**: Capacidad limitada sin conexión a internet

### 2.3 Requisitos Técnicos

#### RT001 - Plataforma
- **Backend**: Python 3.10+ con Flask
- **Frontend**: HTML5, CSS3, JavaScript ES6+
- **Base de datos**: MySQL 8.0+

#### RT002 - Frameworks
- **ORM**: SQLAlchemy para manejo de BD
- **CSS**: Tailwind CSS para estilos
- **JS**: jQuery para manipulación DOM

#### RT003 - Infraestructura
- **Servidor**: Linux/Windows compatible
- **Memoria**: Mínimo 2GB RAM
- **Almacenamiento**: 10GB disponibles

---

## 3. CASOS DE USO DEL SISTEMA

### 3.1 Actores del Sistema

#### Actor Principal: Administrador
- **Responsabilidades**: Gestión completa del sistema
- **Permisos**: Acceso total, edición de registros, gestión de usuarios

#### Actor Secundario: Verificador
- **Responsabilidades**: Confirmación de ingresos a cuenta
- **Permisos**: Confirmar gerencia, visualizar registros

#### Actor Terciario: Vendedor
- **Responsabilidades**: Confirmación de comprobantes
- **Permisos**: Confirmar redes, visualizar asignados

#### Actor Cuaternario: Contabilidad
- **Responsabilidades**: Visualización y reportes
- **Permisos**: Solo lectura, exportación

### 3.2 Casos de Uso Principales

#### CU001: Iniciar Sesión
**Actor**: Todos los usuarios
**Precondiciones**: Usuario registrado en el sistema
**Flujo Principal**:
1. Usuario ingresa credenciales
2. Sistema valida autenticación
3. Sistema carga interfaz según rol
4. Usuario accede al dashboard

**Flujo Alternativo**:
- 2a. Credenciales incorrectas → Mostrar error
- 2b. Usuario bloqueado → Denegar acceso

#### CU002: Confirmar Registro Individual (Redes)
**Actor**: Vendedor, Admin
**Precondiciones**: Registro pendiente de confirmación
**Flujo Principal**:
1. Usuario selecciona registro
2. Ingresa fecha y hora del comprobante
3. Sistema valida formato de fecha
4. Confirma la operación
5. Sistema actualiza estado y auditoría

**Flujo Alternativo**:
- 3a. Formato incorrecto → Solicitar corrección
- 4a. Usuario cancela → Mantener estado original

#### CU003: Confirmar Registro Individual (Gerencia)
**Actor**: Verificador, Admin
**Precondiciones**: Registro confirmado por redes
**Flujo Principal**:
1. Usuario selecciona registro confirmado por redes
2. Ingresa fecha de ingreso a cuenta
3. Sistema valida información
4. Confirma la operación
5. Sistema marca como completamente confirmado

#### CU004: Confirmación Masiva
**Actor**: Vendedor, Verificador
**Precondiciones**: Múltiples registros con fechas completadas
**Flujo Principal**:
1. Usuario visualiza lista de registros
2. Completa fechas en registros pendientes
3. Selecciona "Confirmar masivo"
4. Sistema valida todos los registros
5. Confirma todos simultáneamente

**Flujo Alternativo**:
- 4a. Registros incompletos → Mostrar errores específicos

#### CU005: Exportar Datos
**Actor**: Admin, Verificador, Contabilidad
**Precondiciones**: Registros disponibles en el sistema
**Flujo Principal**:
1. Usuario solicita exportación
2. Sistema consulta todos los registros
3. Genera archivo Excel
4. Descarga automáticamente

#### CU006: Gestión de Usuarios (Admin)
**Actor**: Administrador
**Precondiciones**: Sesión de administrador activa
**Flujo Principal**:
1. Admin accede a mantenimiento
2. Selecciona gestión de usuarios
3. Crea/edita/elimina usuarios
4. Asigna roles correspondientes
5. Sistema actualiza permisos

### 3.3 Casos de Uso Secundarios

#### CU007: Auditoría de Cambios
**Actor**: Administrador
**Flujo Principal**:
1. Admin accede a registros de auditoría
2. Filtra por fecha/usuario/acción
3. Visualiza historial detallado
4. Puede exportar registro de auditoría

#### CU008: Edición de Fechas (Admin)
**Actor**: Administrador
**Precondiciones**: Motivo válido para edición
**Flujo Principal**:
1. Admin selecciona registro a editar
2. Modifica fecha con justificación
3. Ingresa motivo obligatorio
4. Sistema registra en auditoría
5. Actualiza registro con nueva información

### 3.4 Diagramas de Casos de Uso

#### Diagrama General del Sistema
```
                    Sistema de Registro de Caja
    
    Administrador                             Verificador
         |                                        |
         |--- Gestionar Usuarios                  |--- Confirmar Gerencia
         |--- Editar Registros                    |--- Visualizar Registros
         |--- Ver Auditoría                       |--- Exportar Datos
         |--- Confirmar Redes/Gerencia            |
         |--- Exportar Datos                      |
                        |                         |
                        |                         |
                 [Sistema de Caja] ----------------
                        |                         |
                        |                         |
         Vendedor       |                         |    Contabilidad
              |         |                         |         |
              |--- Confirmar Redes               |         |--- Visualizar Registros
              |--- Visualizar Registros          |         |--- Exportar Datos
              |--- Completar Fechas              |
```

#### Diagrama de Casos de Uso por Actor

**Actor: Administrador**
```
    Administrador
         |
         |--- CU001: Iniciar Sesión
         |--- CU002: Gestionar Usuarios
         |--- CU003: Editar Fechas/Registros
         |--- CU004: Confirmar Individual (Redes)
         |--- CU005: Confirmar Individual (Gerencia)
         |--- CU006: Confirmación Masiva
         |--- CU007: Consultar Auditoría
         |--- CU008: Exportar Datos
         |--- CU009: Configurar Sistema
```

**Actor: Verificador**
```
    Verificador
         |
         |--- CU001: Iniciar Sesión
         |--- CU003: Confirmar Individual (Gerencia)
         |--- CU006: Confirmación Masiva (Gerencia)
         |--- CU008: Exportar Datos
         |--- CU010: Visualizar Registros
```

**Actor: Vendedor**
```
    Vendedor
         |
         |--- CU001: Iniciar Sesión
         |--- CU002: Confirmar Individual (Redes)
         |--- CU004: Confirmación Masiva (Redes)
         |--- CU008: Completar Fechas
         |--- CU010: Visualizar Registros
```

**Actor: Contabilidad**
```
    Contabilidad
         |
         |--- CU001: Iniciar Sesión
         |--- CU008: Exportar Datos
         |--- CU010: Visualizar Registros (Solo Lectura)
```

### 3.5 Diagramas de Actividad

#### Flujo de Confirmación Individual (Redes)
```
    [Inicio] 
       |
    [Seleccionar Registro Pendiente]
       |
    [¿Registro Válido?] ----No----> [Mostrar Error] --> [Fin]
       |
      Sí
       |
    [Ingresar Fecha Comprobante]
       |
    [Ingresar Hora Comprobante]
       |
    [¿Datos Válidos?] ----No----> [Mostrar Validación] --> [Corregir Datos]
       |                                                           |
      Sí                                                          |
       |                                                          |
    [Mostrar Modal Confirmación] <----------------------------------
       |
    [¿Usuario Confirma?] ----No----> [Cancelar Operación] --> [Fin]
       |
      Sí
       |
    [Actualizar Estado a "Confirmado Redes"]
       |
    [Registrar en Auditoría]
       |
    [Mostrar Mensaje Éxito]
       |
    [Fin]
```

#### Flujo de Confirmación Individual (Gerencia)
```
    [Inicio] 
       |
    [Seleccionar Registro Confirmado por Redes]
       |
    [¿Registro Válido para Gerencia?] ----No----> [Mostrar Error] --> [Fin]
       |
      Sí
       |
    [Ingresar Fecha Ingreso a Cuenta]
       |
    [¿Fecha Válida?] ----No----> [Mostrar Validación] --> [Corregir Fecha]
       |                                                        |
      Sí                                                       |
       |                                                       |
    [Mostrar Modal Confirmación] <------------------------------
       |
    [¿Usuario Confirma?] ----No----> [Cancelar Operación] --> [Fin]
       |
      Sí
       |
    [Actualizar Estado a "Confirmado Completo"]
       |
    [Registrar en Auditoría]
       |
    [Mostrar Mensaje Éxito]
       |
    [Fin]
```

#### Flujo de Confirmación Masiva
```
    [Inicio] 
       |
    [Verificar Registros con Fechas Completas]
       |
    [¿Hay Registros Válidos?] ----No----> [Mostrar "Sin Registros"] --> [Fin]
       |
      Sí
       |
    [Mostrar Lista de Registros a Confirmar]
       |
    [Usuario Revisa Lista]
       |
    [¿Usuario Confirma Masivo?] ----No----> [Cancelar Operación] --> [Fin]
       |
      Sí
       |
    [Iniciar Transacción BD]
       |
    [Para cada registro:]
       |
    [Actualizar Estado] --> [¿Error?] ----Sí----> [Rollback] --> [Mostrar Error] --> [Fin]
       |                        |
    [Registrar Auditoría]      No
       |                        |
    [¿Más Registros?] ----Sí----|
       |
      No
       |
    [Commit Transacción]
       |
    [Mostrar Resultado Masivo]
       |
    [Fin]
```

---

## 4. INFORME GENERAL DEL SISTEMA

### 4.1 Visión General

El Sistema de Registro de Caja es una aplicación web desarrollada en Flask que centraliza la gestión financiera del Castillo de Chancay. Implementa un flujo de confirmación en dos niveles (Redes y Gerencia) con control granular de permisos.

### 4.2 Objetivos del Sistema

#### Objetivos Primarios
1. **Centralizar** la gestión de registros de caja
2. **Automatizar** los procesos de confirmación
3. **Auditar** todas las operaciones realizadas
4. **Controlar** el acceso mediante roles específicos

#### Objetivos Secundarios
1. **Optimizar** tiempos de procesamiento
2. **Reducir** errores humanos
3. **Facilitar** la generación de reportes
4. **Mejorar** la trazabilidad de operaciones

### 4.3 Alcance del Sistema

#### Incluye:
- Gestión completa de registros de caja
- Sistema de confirmación multinivel
- Auditoría automática de cambios
- Gestión de usuarios y permisos
- Exportación de datos
- Interfaz web responsiva

#### No Incluye:
- Integración con sistemas bancarios
- Procesamiento de pagos en línea
- Módulo de inventarios
- Contabilidad avanzada

### 4.4 Beneficios Esperados

#### Operacionales
- Reducción del 70% en tiempo de confirmaciones
- Eliminación de errores de transcripción
- Mejora en trazabilidad de operaciones

#### Administrativos
- Control granular de permisos
- Auditoría completa automática
- Reportes en tiempo real

#### Estratégicos
- Cumplimiento de normativas de auditoría
- Base para futuras integraciones
- Mejora en toma de decisiones

---

## 5. ARQUITECTURA Y DISEÑO

### 5.1 Arquitectura del Sistema

#### Patrón Arquitectónico: MVC (Model-View-Controller)

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│     VISTA       │    │   CONTROLADOR   │    │     MODELO      │
│   (Templates)   │◄──►│   (Routes)      │◄──►│   (Database)    │
│                 │    │                 │    │                 │
│ - HTML/Jinja2   │    │ - Flask Routes  │    │ - SQLAlchemy    │
│ - JavaScript    │    │ - Business Logic│    │ - MySQL         │
│ - CSS/Tailwind  │    │ - Validation    │    │ - Models        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### 5.2 Componentes del Sistema

#### Capa de Presentación
- **Templates**: Jinja2 para renderizado dinámico
- **Frontend**: HTML5, CSS3, JavaScript ES6+
- **Frameworks**: Tailwind CSS, jQuery
- **Responsive**: Bootstrap components

#### Capa de Lógica de Negocio
- **Controllers**: Manejo de reglas de negocio
- **Routes**: Definición de endpoints REST
- **Middleware**: Autenticación y autorización
- **Validation**: Sanitización de datos

#### Capa de Datos
- **ORM**: SQLAlchemy para abstracción de BD
- **Database**: MySQL 8.0+
- **Migrations**: Flask-Migrate
- **Connections**: Pool de conexiones

### 5.3 Modelo de Datos

#### Entidades Principales

**usuarios**
```sql
id (VARCHAR) PK
nombre (VARCHAR)
correo (VARCHAR) UNIQUE
contrasena (VARCHAR) -- hasheada
rol_id (INT) FK
session_active (BOOLEAN)
```

**registros_ventas**
```sql
id (INT) PK
recibo (VARCHAR) UNIQUE
monto (DECIMAL)
detalle (TEXT)
confirmado (BOOLEAN)
confirmado_redes (BOOLEAN)
fecha_registro_pago (DATE)
fecha_comprobante (DATETIME)
fecha_ingreso_cuenta (DATE)
fecha_confirmacion_redes (DATETIME)
fecha_confirmacion_gerencia (DATETIME)
-- FK relationships
empresa_id, area_id, medio_pago_id, etc.
```

**auditoria_registros_ventas**
```sql
id (INT) PK
registro_venta_id (INT) FK
usuario_id (VARCHAR) FK
accion (ENUM)
campo_modificado (VARCHAR)
valor_anterior (TEXT)
valor_nuevo (TEXT)
fecha_cambio (DATETIME)
motivo_cambio (TEXT)
ip_usuario (VARCHAR)
```

### 5.4 Flujo de Datos

#### Confirmación Individual
```
Usuario → Frontend → Route → Controller → Model → Database
                 ↓
              Auditoría → Trigger → auditoria_registros_ventas
```

#### Confirmación Masiva
```
Frontend (AJAX) → Route → Controller → Transaction → Batch Update
                                          ↓
                                    Audit Context → Database
```

### 5.5 Diagrama de Clases del Sistema

#### Estructura de Clases Principal

```
┌─────────────────────────────────────────────────────────────────┐
│                        MODELO DE DATOS                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────┐ │
│  │     Usuario     │    │ RegistroVenta   │    │   Auditoria │ │
│  │─────────────────│    │─────────────────│    │─────────────│ │
│  │ + id: str       │    │ + id: int       │    │ + id: int   │ │
│  │ + nombre: str   │ 1  │ + recibo: str   │ 1  │ + accion    │ │
│  │ + correo: str   │──→ │ + monto: decimal│──→ │ + fecha     │ │
│  │ + contrasena    │    │ + detalle: text │    │ + usuario   │ │
│  │ + rol_id: int   │    │ + confirmado    │    │ + motivo    │ │
│  │ + session_active│    │ + empresa_id    │    │ + ip        │ │
│  │─────────────────│    │ + area_id       │    │─────────────│ │
│  │ + authenticate()│    │ + medio_pago_id │    │ + registrar()│ │
│  │ + check_role()  │    │ + fecha_registro│    │ + consultar()│ │
│  │ + logout()      │    │ + fecha_confirm │    │             │ │
│  │                 │    │─────────────────│    │             │ │
│  │                 │    │ + confirmar()   │    │             │ │
│  │                 │    │ + validar()     │    │             │ │
│  └─────────────────┘    │ + exportar()    │    │             │ │
│           │              └─────────────────┘    │             │ │
│           │                       │             │             │ │
│           ▼                       ▼             ▼             │ │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────┐ │
│  │      Rol        │    │    Empresa      │    │    Area     │ │
│  │─────────────────│    │─────────────────│    │─────────────│ │
│  │ + id: int       │    │ + id: int       │    │ + id: int   │ │
│  │ + nombre: str   │    │ + nombre: str   │    │ + nombre    │ │
│  │ + descripcion   │    │ + codigo: str   │    │ + codigo    │ │
│  │ + permisos      │    │ + activo: bool  │    │ + activo    │ │
│  │─────────────────│    │─────────────────│    │─────────────│ │
│  │ + get_permisos()│    │ + get_activas() │    │ + get_todas()│ │
│  └─────────────────┘    └─────────────────┘    └─────────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                       CONTROLADORES                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────┐ │
│  │ AuditoriaCtrl   │    │   AdminCtrl     │    │  AuthCtrl   │ │
│  │─────────────────│    │─────────────────│    │─────────────│ │
│  │ + get_registros()│    │ + gestionar_usr()│    │ + login()   │ │
│  │ + confirmar_ind()│    │ + editar_fecha() │    │ + logout()  │ │
│  │ + confirmar_mas()│    │ + ver_auditoria()│    │ + verificar()│ │
│  │ + exportar_data()│    │ + configurar()   │    │ + session() │ │
│  │ + aplicar_filtro()│   │ + mantenimiento()│    │─────────────│ │
│  │─────────────────│    │─────────────────│    │             │ │
│  │                 │    │                 │    │             │ │
│  └─────────────────┘    └─────────────────┘    └─────────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                         SERVICIOS                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────┐ │
│  │ DatabaseService │    │  ExportService  │    │ AuditService│ │
│  │─────────────────│    │─────────────────│    │─────────────│ │
│  │ + get_connection()│   │ + to_excel()    │    │ + log()     │ │
│  │ + execute_query()│    │ + format_data() │    │ + context() │ │
│  │ + transaction() │    │ + generate()    │    │ + clear()   │ │
│  │ + close()       │    │─────────────────│    │─────────────│ │
│  │─────────────────│    │                 │    │             │ │
│  │                 │    │                 │    │             │ │
│  └─────────────────┘    └─────────────────┘    └─────────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

#### Relaciones Entre Clases

```
Usuario 1───────────* RegistroVenta
   │                      │
   │                      │
   ▼                      ▼
  Rol                 Auditoria
   │                      ▲
   │                      │
   └──────────────────────┘

Empresa 1───────────* RegistroVenta
Area    1───────────* RegistroVenta
MedioPago 1─────────* RegistroVenta
```

#### Diagrama de Componentes del Sistema

```
┌─────────────────────────────────────────────────────────────────┐
│                     FRONTEND LAYER                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐│
│ │   HTML5     │ │ Tailwind CSS│ │  jQuery     │ │ JavaScript  ││
│ │ Templates   │ │   Styles    │ │   AJAX      │ │   Logic     ││
│ └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘│
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                    APPLICATION LAYER                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐│
│ │   Flask     │ │   Routes    │ │Controllers  │ │Middleware   ││
│ │ Application │ │  Endpoints  │ │ Business    │ │ Auth/Valid  ││
│ │   Factory   │ │   /login    │ │   Logic     │ │  Session    ││
│ │             │ │ /auditoria  │ │             │ │   Mgmt      ││
│ └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘│
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                      DATA LAYER                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐│
│ │ SQLAlchemy  │ │   Models    │ │   MySQL     │ │   Triggers  ││
│ │    ORM      │ │ Definition  │ │  Database   │ │  Procedures ││
│ │ Connection  │ │ Validation  │ │  Tables     │ │  Audit Log  ││
│ │    Pool     │ │ Relations   │ │  Indexes    │ │   Context   ││
│ └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘│
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 6. PROTOTIPADO DEL SISTEMA

### 6.1 Wireframes Principales

#### Pantalla de Login
```
┌─────────────────────────────────────┐
│           CASTILLO DE CHANCAY       │
│               [LOGO]                │
│                                     │
│  Email:    [________________]       │
│  Password: [________________]       │
│                                     │
│            [  INGRESAR  ]           │
│                                     │
│  ¿Olvidaste tu contraseña?          │
└─────────────────────────────────────┘
```

#### Dashboard Principal
```
┌────────────────────────────────────────────────────────┐
│ Gestión de Caja | [Usuario]              [LOGOUT]     │
├────────────────────────────────────────────────────────┤
│ [Auditoría] [Registros Auditoría] [Mantenimiento]     │
├────────────────────────────────────────────────────────┤
│                                                        │
│ Filtros: [Fecha desde] [Fecha hasta] [Buscar]         │
│                                                        │
│ [Por Confirmar] [Confirmados] [Confirmar Masivo]      │
│                                                        │
│ ┌────┬──────┬────────┬────────┬──────────┬─────────┐   │
│ │ ID │Recibo│Empresa │ Monto  │  Estado  │Acciones │   │
│ ├────┼──────┼────────┼────────┼──────────┼─────────┤   │
│ │001 │R-001 │Emp A   │1500.00 │Pendiente │[Confirm]│   │
│ │002 │R-002 │Emp B   │2500.00 │Pendiente │[Confirm]│   │
│ └────┴──────┴────────┴────────┴──────────┴─────────┘   │
│                                                        │
│ [Anterior] Página 1 de 10 [Siguiente]                 │
└────────────────────────────────────────────────────────┘
```

#### Modal de Confirmación
```
┌─────────────────────────────────────┐
│  Confirmar desde Redes              │
├─────────────────────────────────────┤
│                                     │
│  Fecha: [2025-08-23] [▼]           │
│  Hora:  [14:30]      [▼]           │
│                                     │
│  ¿Confirmar esta transacción?      │
│                                     │
│  [CANCELAR]    [SÍ, CONFIRMAR]     │
└─────────────────────────────────────┘
```

### 6.2 Flujo de Navegación

#### Flujo Principal (Vendedor)
```
Login → Dashboard → Filtrar Registros → Confirmar Individual
  ↓                     ↓                      ↓
Logout ← Dashboard ← Ver Confirmados ← Éxito/Error
```

#### Flujo Administrativo
```
Login → Dashboard → Mantenimiento → Gestión Usuarios
  ↓         ↓            ↓              ↓
Logout ← Dashboard ← Auditoría ← Modificar Registro
```

### 6.3 Elementos de Interfaz

#### Componentes Reutilizables
- **Botones**: Primarios (azul), Secundarios (gris), Peligro (rojo)
- **Formularios**: Validación en tiempo real, placeholders descriptivos
- **Tablas**: Paginación, ordenamiento, filtros
- **Modales**: Confirmación, edición, información
- **Alertas**: Éxito (verde), Error (rojo), Información (azul)

#### Paleta de Colores
- **Primario**: #7c4e1a (marrón principal)
- **Secundario**: #b07c40 (marrón claro)
- **Éxito**: #10b981 (verde)
- **Error**: #ef4444 (rojo)
- **Información**: #3b82f6 (azul)

### 6.4 Capturas de Pantalla del Sistema

#### Pantalla de Inicio de Sesión
```
[IMAGEN: login_screen.png]
- Interfaz limpia y profesional
- Campos de email y contraseña
- Logo del Castillo de Chancay
- Mensaje de validación en tiempo real
- Botón de acceso principal
```

#### Dashboard Principal - Vista Administrador
```
[IMAGEN: dashboard_admin.png]
- Menú de navegación completo
- Filtros avanzados de búsqueda
- Tabla de registros con paginación
- Botones de acción por registro
- Indicadores de estado visual
- Panel de confirmación masiva
```

#### Modal de Confirmación Individual
```
[IMAGEN: modal_confirmacion.png]
- Formulario de fecha y hora
- Validación en tiempo real
- Botones de acción claros
- Información del registro
- Confirmación de seguridad
```

#### Vista de Auditoría
```
[IMAGEN: auditoria_view.png]
- Tabla detallada de cambios
- Filtros por usuario y fecha
- Información completa de modificaciones
- Exportación de datos disponible
- Historial completo de acciones
```

#### Panel de Mantenimiento
```
[IMAGEN: mantenimiento_panel.png]
- Gestión de usuarios
- Configuración de roles
- Administración de entidades
- Herramientas de sistema
- Opciones de configuración
```

#### Vista Móvil - Responsive Design
```
[IMAGEN: mobile_view.png]
- Adaptación completa a dispositivos móviles
- Menú colapsable
- Tablas responsivas
- Formularios optimizados
- Navegación táctil
```

#### Reportes y Exportación
```
[IMAGEN: export_excel.png]
- Generación automática de Excel
- Formato profesional de datos
- Filtros aplicados al reporte
- Descarga inmediata
- Datos completos y ordenados
```

#### Estados de Confirmación Visual
```
[IMAGEN: estados_confirmacion.png]
- Indicadores de color por estado
- Iconos descriptivos
- Progreso de confirmación
- Diferenciación clara de roles
- Feedback visual inmediato
```

### 6.5 Flujos de Interacción Detallados

#### Secuencia de Confirmación Individual
```
Usuario          Frontend         Backend         Database
  |                 |                |               |
  |-- Click Confirmar ->              |               |
  |                 |-- AJAX Request ->              |
  |                 |                |-- UPDATE ---->|
  |                 |                |<-- Result ----|
  |                 |<-- Response ---|               |
  |<-- UI Update ---|                |               |
  |-- Success Msg --|                |               |
```

#### Secuencia de Confirmación Masiva
```
Usuario          Frontend         Backend         Database
  |                 |                |               |
  |-- Complete Dates ->              |               |
  |-- Click Masivo -->               |               |
  |                 |-- AJAX Batch -->              |
  |                 |                |-- BEGIN ----->|
  |                 |                |-- UPDATE 1 -->|
  |                 |                |-- UPDATE 2 -->|
  |                 |                |-- UPDATE N -->|
  |                 |                |-- COMMIT ---->|
  |                 |<-- Results ----|               |
  |<-- Batch Result ---|              |               |
```

---

## 7. PLAN DE PRUEBAS

### 7.1 Estrategia de Pruebas

#### Tipos de Pruebas
1. **Pruebas Unitarias**: Funciones individuales
2. **Pruebas de Integración**: Componentes combinados
3. **Pruebas de Sistema**: Sistema completo
4. **Pruebas de Aceptación**: Requisitos del usuario

### 7.2 Casos de Prueba

#### CP001: Login Exitoso
- **Objetivo**: Verificar autenticación correcta
- **Precondiciones**: Usuario válido registrado
- **Pasos**:
  1. Ingresar credenciales correctas
  2. Presionar "Ingresar"
- **Resultado Esperado**: Redirección a dashboard
- **Criterio de Éxito**: Usuario autenticado correctamente

#### CP002: Login Fallido
- **Objetivo**: Verificar manejo de credenciales incorrectas
- **Precondiciones**: Sistema funcionando
- **Pasos**:
  1. Ingresar credenciales incorrectas
  2. Presionar "Ingresar"
- **Resultado Esperado**: Mensaje de error
- **Criterio de Éxito**: Acceso denegado

#### CP003: Confirmación Individual
- **Objetivo**: Confirmar registro individual
- **Precondiciones**: Usuario vendedor autenticado
- **Pasos**:
  1. Seleccionar registro pendiente
  2. Ingresar fecha y hora
  3. Confirmar operación
- **Resultado Esperado**: Estado actualizado
- **Criterio de Éxito**: Registro marcado como confirmado

#### CP004: Confirmación Masiva
- **Objetivo**: Confirmar múltiples registros
- **Precondiciones**: Registros con fechas completadas
- **Pasos**:
  1. Completar fechas en múltiples registros
  2. Presionar "Confirmar masivo"
  3. Confirmar en modal
- **Resultado Esperado**: Todos los registros confirmados
- **Criterio de Éxito**: Estados actualizados masivamente

#### CP005: Auditoría de Cambios
- **Objetivo**: Verificar registro de auditoría
- **Precondiciones**: Cambio realizado en registro
- **Pasos**:
  1. Realizar modificación en registro
  2. Consultar tabla de auditoría
- **Resultado Esperado**: Cambio registrado
- **Criterio de Éxito**: Auditoría completa y precisa

### 7.3 Pruebas de Rendimiento

#### Carga Normal
- **Usuarios Concurrentes**: 25
- **Transacciones/min**: 500
- **Tiempo de Respuesta**: < 2 segundos

#### Carga Pico
- **Usuarios Concurrentes**: 50
- **Transacciones/min**: 1000
- **Tiempo de Respuesta**: < 5 segundos

### 7.4 Pruebas de Seguridad

#### Autenticación
- Verificar hash de contraseñas
- Probar timeout de sesiones
- Validar control de acceso por roles

#### Validación de Datos
- Inyección SQL
- XSS (Cross-Site Scripting)
- CSRF (Cross-Site Request Forgery)

---

## 8. MANUAL DE CONFIGURACIÓN BD

### 8.1 Requisitos de Base de Datos

#### Software Necesario
- **MySQL Server**: 8.0 o superior
- **Cliente MySQL**: MySQL Workbench o similar
- **Drivers**: mysql-connector-python

#### Configuración del Servidor
```sql
-- Configuraciones recomendadas
SET GLOBAL innodb_buffer_pool_size = 128M;
SET GLOBAL max_connections = 200;
SET GLOBAL wait_timeout = 28800;
SET GLOBAL interactive_timeout = 28800;
```

### 8.2 Instalación de Base de Datos

#### Paso 1: Crear Base de Datos
```bash
mysql -u root -p
```

```sql
CREATE DATABASE IF NOT EXISTS gestion_caja 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE gestion_caja;
```

#### Paso 2: Ejecutar Script de Creación
```bash
mysql -u root -p gestion_caja < data/bd_cajalima.sql
```

#### Paso 3: Verificar Instalación
```sql
SHOW TABLES;
SELECT COUNT(*) FROM usuarios;
SELECT COUNT(*) FROM roles;
```

### 8.3 Diagrama Entidad-Relación (ER)

#### Modelo Relacional Completo

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           MODELO DE BASE DE DATOS                              │
│                          Sistema de Registro de Caja                          │
└─────────────────────────────────────────────────────────────────────────────────┘

         ┌─────────────────┐                    ┌─────────────────┐
         │      roles      │                    │    usuarios     │
         │─────────────────│                    │─────────────────│
         │ PK id (INT)     │ 1              1..* │ PK id (VARCHAR) │
         │    nombre       │ ────────────────────│    nombre       │
         │    descripcion  │                    │    correo       │
         │    permisos     │                    │    contrasena   │
         │    activo       │                    │ FK rol_id       │
         └─────────────────┘                    │    session_act  │
                                                │    created_at   │
                                                │    updated_at   │
                                                └─────────────────┘
                                                         │
                                                         │ 1
                                                         │
                                                         │ *
                ┌─────────────────┐                    ┌─────────────────┐
                │    empresas     │ 1              1..* │ registros_ventas│
                │─────────────────│ ────────────────────│─────────────────│
                │ PK id (INT)     │                    │ PK id (INT)     │
                │    nombre       │                    │    recibo       │
                │    codigo       │                    │    monto        │
                │    activo       │                    │    detalle      │
                └─────────────────┘                    │    confirmado   │
                                                       │    confirmado_r │
                ┌─────────────────┐                    │ FK empresa_id   │
                │     areas       │ 1              1..*│ FK area_id      │
                │─────────────────│ ────────────────────│ FK centro_costo │
                │ PK id (INT)     │                    │ FK entidad_banc │
                │    nombre       │                    │ FK medio_pago   │
                │    codigo       │                    │ FK usuario_crea │
                │    activo       │                    │    fecha_reg_p  │
                └─────────────────┘                    │    fecha_comprob│
                                                       │    fecha_ing_cta│
                ┌─────────────────┐                    │    fecha_conf_r │
                │ centros_costos  │ 1              1..*│    fecha_conf_g │
                │─────────────────│ ────────────────────│    created_at   │
                │ PK id (INT)     │                    │    updated_at   │
                │    nombre       │                    └─────────────────┘
                │    codigo       │                             │
                │    activo       │                             │ 1
                └─────────────────┘                             │
                                                                │
                ┌─────────────────┐                             │ *
                │entidades_bancarias│ 1                        │
                │─────────────────│ ──────────────────────────┐ │
                │ PK id (INT)     │                          │ │
                │    nombre       │                          │ │
                │    codigo       │                          │ │
                │    activo       │                          │ │
                └─────────────────┘                          │ │
                                                             │ │
                ┌─────────────────┐                          │ │
                │  medios_pagos   │ 1                        │ │
                │─────────────────│ ─────────────────────────┘ │
                │ PK id (INT)     │                           │
                │    nombre       │                           │
                │    codigo       │                           │
                │    activo       │                           │
                └─────────────────┘                           │
                                                              │
                                                              │
            ┌─────────────────────────────────────────────────┘
            │
            │ 1
            │
            │ *
         ┌─────────────────┐
         │auditoria_registros_ventas│
         │─────────────────│
         │ PK id (INT)     │
         │ FK registro_venta_id │
         │ FK usuario_id   │
         │    accion       │
         │    campo_modif  │
         │    valor_anterior│
         │    valor_nuevo  │
         │    fecha_cambio │
         │    motivo_cambio│
         │    ip_usuario   │
         │    created_at   │
         └─────────────────┘
```

#### Descripción de Relaciones

**Relaciones Principales:**
- `usuarios` ←→ `roles` (Muchos a Uno)
- `registros_ventas` ←→ `usuarios` (Muchos a Uno) 
- `registros_ventas` ←→ `empresas` (Muchos a Uno)
- `registros_ventas` ←→ `areas` (Muchos a Uno)
- `registros_ventas` ←→ `centros_costos` (Muchos a Uno)
- `registros_ventas` ←→ `entidades_bancarias` (Muchos a Uno)
- `registros_ventas` ←→ `medios_pagos` (Muchos a Uno)
- `auditoria_registros_ventas` ←→ `registros_ventas` (Muchos a Uno)
- `auditoria_registros_ventas` ←→ `usuarios` (Muchos a Uno)

#### Constraints y Reglas de Negocio

**Claves Primarias:**
- Todas las tablas tienen claves primarias auto-incrementales
- `usuarios.id` es VARCHAR para mayor flexibilidad

**Claves Foráneas:**
- Todas las FK tienen restricciones de integridad referencial
- ON DELETE RESTRICT para prevenir eliminaciones en cascada
- ON UPDATE CASCADE para actualizaciones automáticas

**Índices Recomendados:**
```sql
-- Índices para optimizar consultas frecuentes
CREATE INDEX idx_registros_fecha ON registros_ventas(fecha_registro_pago);
CREATE INDEX idx_registros_empresa ON registros_ventas(empresa_id);
CREATE INDEX idx_registros_usuario ON registros_ventas(usuario_creacion_id);
CREATE INDEX idx_auditoria_fecha ON auditoria_registros_ventas(fecha_cambio);
CREATE INDEX idx_auditoria_registro ON auditoria_registros_ventas(registro_venta_id);
CREATE INDEX idx_usuarios_email ON usuarios(correo);
```

### 8.4 Configuración de Usuarios

#### Usuario de Aplicación
```sql
CREATE USER 'app_caja'@'localhost' IDENTIFIED BY 'password_seguro';
GRANT SELECT, INSERT, UPDATE, DELETE ON gestion_caja.* TO 'app_caja'@'localhost';
FLUSH PRIVILEGES;
```

#### Usuario de Solo Lectura
```sql
CREATE USER 'readonly_caja'@'localhost' IDENTIFIED BY 'readonly_password';
GRANT SELECT ON gestion_caja.* TO 'readonly_caja'@'localhost';
FLUSH PRIVILEGES;
```

### 8.4 Triggers y Procedimientos

#### Trigger de Auditoría
```sql
DELIMITER //
CREATE TRIGGER audit_registros_ventas_update
AFTER UPDATE ON registros_ventas
FOR EACH ROW
BEGIN
    INSERT INTO auditoria_registros_ventas (
        registro_venta_id, usuario_id, accion, 
        campo_modificado, valor_anterior, valor_nuevo,
        ip_usuario, motivo_cambio
    ) VALUES (
        NEW.id, @audit_user_id, 'UPDATE',
        'multiple_fields', 'old_values', 'new_values',
        @audit_ip, @audit_reason
    );
END//
DELIMITER ;
```

#### Procedimiento de Contexto de Auditoría
```sql
DELIMITER //
CREATE PROCEDURE SetAuditContext(
    IN p_user_id VARCHAR(100),
    IN p_reason TEXT,
    IN p_ip VARCHAR(45)
)
BEGIN
    SET @audit_user_id = p_user_id;
    SET @audit_reason = p_reason;
    SET @audit_ip = p_ip;
END//

CREATE PROCEDURE ClearAuditContext()
BEGIN
    SET @audit_user_id = NULL;
    SET @audit_reason = NULL;
    SET @audit_ip = NULL;
END//
DELIMITER ;
```

### 8.5 Mantenimiento de Base de Datos

#### Backup Diario
```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
mysqldump -u root -p gestion_caja > backup_caja_$DATE.sql
```

#### Limpieza de Logs
```sql
-- Mantener solo auditoría de últimos 12 meses
DELETE FROM auditoria_registros_ventas 
WHERE fecha_cambio < DATE_SUB(NOW(), INTERVAL 12 MONTH);
```

#### Optimización de Tablas
```sql
OPTIMIZE TABLE registros_ventas;
OPTIMIZE TABLE auditoria_registros_ventas;
ANALYZE TABLE usuarios;
```

---

## 9. MANUAL TÉCNICO DE CONFIGURACIÓN

### 9.1 Requisitos del Sistema

#### Servidor de Aplicación
- **SO**: Linux Ubuntu 20.04+ / Windows Server 2019+
- **Python**: 3.10 o superior
- **RAM**: Mínimo 2GB, Recomendado 4GB
- **Almacenamiento**: 10GB disponibles
- **Red**: Puerto 5000 disponible

#### Dependencias del Sistema
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip python3-venv
sudo apt install mysql-server mysql-client
sudo apt install git curl wget

# CentOS/RHEL
sudo yum install python3 python3-pip
sudo yum install mysql-server mysql
sudo yum install git curl wget
```

### 9.2 Instalación del Sistema

#### Paso 1: Clonar Repositorio
```bash
git clone https://github.com/DesarrolloChancay/RegistroDeCaja.git
cd RegistroDeCaja
```

#### Paso 2: Configurar Entorno Virtual
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows
```

#### Paso 3: Instalar Dependencias
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### Paso 4: Configurar Variables de Entorno
```bash
# Crear archivo .env
cat > .env << EOF
FLASK_APP=run.py
FLASK_ENV=production
SECRET_KEY=your_very_secret_key_here
DATABASE_URL=mysql://user:password@localhost/gestion_caja
MYSQL_HOST=localhost
MYSQL_USER=app_caja
MYSQL_PASSWORD=password_seguro
MYSQL_DB=gestion_caja
EOF
```

### 9.3 Configuración de Producción

#### Servidor Web (Nginx)
```nginx
server {
    listen 80;
    server_name tu-dominio.com;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    location /static {
        alias /path/to/RegistroDeCaja/app/static;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

#### Supervisor (Gestión de Procesos)
```ini
[program:registro_caja]
command=/path/to/RegistroDeCaja/venv/bin/python run.py
directory=/path/to/RegistroDeCaja
user=www-data
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/registro_caja.log
```

#### Servicio Systemd
```ini
[Unit]
Description=Registro de Caja Flask App
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/RegistroDeCaja
Environment=PATH=/path/to/RegistroDeCaja/venv/bin
ExecStart=/path/to/RegistroDeCaja/venv/bin/python run.py
Restart=always

[Install]
WantedBy=multi-user.target
```

### 9.4 Configuración de Seguridad

#### Firewall (UFW)
```bash
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
sudo ufw enable
```

#### SSL/TLS (Let's Encrypt)
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d tu-dominio.com
```

#### Configuración de Base de Datos Segura
```sql
-- Cambiar contraseñas por defecto
ALTER USER 'root'@'localhost' IDENTIFIED BY 'nueva_password_segura';

-- Remover usuarios anónimos
DELETE FROM mysql.user WHERE User='';

-- Remover base de datos de prueba
DROP DATABASE IF EXISTS test;

-- Recargar privilegios
FLUSH PRIVILEGES;
```

### 9.5 Monitoreo y Logs

#### Configuración de Logs
```python
# app/config.py
import logging
from logging.handlers import RotatingFileHandler

if not app.debug:
    file_handler = RotatingFileHandler('logs/registro_caja.log', 
                                     maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
```

#### Monitoreo con Cron
```bash
# Verificar estado del servicio cada 5 minutos
*/5 * * * * systemctl is-active --quiet registro_caja || systemctl restart registro_caja

# Backup diario de base de datos
0 2 * * * /path/to/backup_script.sh

# Limpieza de logs semanalmente
0 0 * * 0 find /var/log -name "*.log" -mtime +30 -delete
```

---

## 10. MANUAL DE USUARIO

### 10.1 Introducción al Sistema

El Sistema de Registro de Caja es una herramienta web diseñada para gestionar y auditar las transacciones financieras del Castillo de Chancay. Permite el control granular de confirmaciones y mantiene un registro completo de auditoría.

### 10.2 Acceso al Sistema

#### Inicio de Sesión
1. Abrir navegador web
2. Navegar a la URL del sistema
3. Ingresar credenciales:
   - **Email**: Su correo electrónico registrado
   - **Contraseña**: Su contraseña personal
4. Hacer clic en "Ingresar"

#### Tipos de Usuario
- **Administrador**: Acceso completo al sistema
- **Verificador**: Confirmación de ingresos a cuenta
- **Vendedor**: Confirmación de comprobantes
- **Contabilidad**: Solo visualización y exportes

### 10.3 Navegación Principal

#### Dashboard
Al iniciar sesión, se muestra el dashboard principal con:
- **Filtros**: Para buscar registros específicos
- **Pestañas**: "Por Confirmar" y "Confirmados"
- **Tabla de Registros**: Lista de transacciones
- **Paginación**: Navegación entre páginas

#### Menú Principal
- **Auditoría**: Panel principal de trabajo
- **Registros de Auditoría**: Historial de cambios (Solo Admin)
- **Mantenimiento**: Gestión del sistema (Solo Admin)

### 10.4 Funciones por Rol

#### 10.4.1 Vendedor

**Confirmar Comprobante Individual**
1. Localizar registro pendiente
2. Hacer clic en el campo "Fecha"
3. Seleccionar fecha del comprobante
4. Ingresar hora en campo "Hora"
5. Hacer clic en "Confirmar desde Redes"
6. Confirmar en el modal que aparece

**Confirmación Masiva**
1. Completar fechas y horas en múltiples registros
2. Hacer clic en "Confirmar masivo"
3. Revisar lista de registros a confirmar
4. Confirmar operación en modal
5. Esperar mensaje de confirmación

#### 10.4.2 Verificador

**Confirmar Ingreso a Cuenta**
1. Seleccionar pestaña "Por Confirmar"
2. Localizar registro confirmado por redes
3. Ingresar fecha de ingreso a cuenta
4. Hacer clic en "Confirmar desde Gerencia"
5. Confirmar operación

**Confirmación Masiva de Gerencia**
1. Completar fechas de ingreso en múltiples registros
2. Usar botón "Confirmar masivo"
3. Revisar y confirmar operación

#### 10.4.3 Administrador

**Editar Registros**
1. Localizar registro a editar
2. Modificar fecha/hora necesaria
3. Ingresar motivo obligatorio
4. Guardar cambios
5. Verificar actualización en auditoría

**Gestión de Usuarios**
1. Acceder a "Mantenimiento"
2. Seleccionar "Usuarios"
3. Agregar/Editar/Eliminar usuarios
4. Asignar roles apropiados

**Visualizar Auditoría**
1. Acceder a "Registros de Auditoría"
2. Filtrar por fecha/usuario/acción
3. Revisar cambios realizados
4. Exportar si es necesario

#### 10.4.4 Contabilidad

**Visualizar Registros**
1. Navegar por las pestañas disponibles
2. Usar filtros para encontrar información específica
3. Revisar estados de confirmación

**Exportar Datos**
1. Hacer clic en "Exportar"
2. Esperar generación del archivo
3. Descargar Excel generado
4. Revisar formato de datos

### 10.5 Funciones Comunes

#### Filtrar Registros
1. **Por Fecha**: Usar campos "Fecha desde" y "Fecha hasta"
2. **Por Texto**: Usar buscador general
3. **Por Estado**: Seleccionar pestaña correspondiente
4. Hacer clic en "Buscar" o automático

#### Ordenar Registros
1. En pestaña "Confirmados", usar botón de orden
2. Alternar entre ascendente/descendente
3. Visualizar indicador de orden aplicado

#### Navegar Páginas
1. Usar botones "Anterior"/"Siguiente"
2. Seleccionar número de página específico
3. Cambiar cantidad de registros por página

### 10.6 Mensajes del Sistema

#### Mensajes de Éxito
- **Verde**: Operación completada correctamente
- **Duración**: 3 segundos automático

#### Mensajes de Error
- **Rojo**: Error en la operación
- **Requiere**: Acción del usuario para continuar

#### Confirmaciones
- **Modal**: Para operaciones críticas
- **Requiere**: Confirmación explícita del usuario

### 10.7 Buenas Prácticas

#### Seguridad
1. Cerrar sesión al terminar
2. No compartir credenciales
3. Reportar actividad sospechosa

#### Uso Eficiente
1. Usar filtros para encontrar registros rápidamente
2. Completar fechas antes de confirmación masiva
3. Verificar datos antes de confirmar

#### Mantenimiento
1. Reportar errores al administrador
2. Mantener navegador actualizado
3. Limpiar cache periódicamente

---

## 11. ANEXOS

### Anexo A: Glosario de Términos

**Auditoría**: Registro automático de cambios realizados en el sistema
**Confirmación**: Proceso de validación de una transacción financiera
**Dashboard**: Panel principal de control del sistema
**Middleware**: Componente intermedio entre la interfaz y la base de datos
**ORM**: Object-Relational Mapping, abstracción de base de datos
**Rol**: Conjunto de permisos asignados a un usuario
**Trigger**: Procedimiento automático ejecutado en la base de datos
**Workflow**: Flujo de trabajo definido en el sistema

### Anexo B: Códigos de Error Comunes

| Código | Descripción | Solución |
|--------|-------------|----------|
| 401 | No autorizado | Verificar credenciales |
| 403 | Acceso denegado | Contactar administrador |
| 404 | Registro no encontrado | Verificar ID del registro |
| 500 | Error interno del servidor | Reportar a soporte técnico |

### Anexo C: Diagramas y Documentación Visual

#### Diagramas Incluidos en Este Documento

**Sección 3 - Casos de Uso:**
- Diagrama General del Sistema
- Diagramas de Casos de Uso por Actor
- Diagramas de Actividad (Confirmación Individual y Masiva)

**Sección 5 - Arquitectura:**
- Diagrama de Clases del Sistema
- Diagrama de Componentes
- Arquitectura MVC

**Sección 6 - Prototipado:**
- Capturas de Pantalla del Sistema
- Flujos de Interacción
- Secuencias de Confirmación

**Sección 8 - Base de Datos:**
- Diagrama Entidad-Relación (ER) Completo
- Modelo Relacional
- Esquema de Índices

#### Ubicación de Archivos de Imagen Recomendada

```
docs/
├── images/
│   ├── screenshots/
│   │   ├── login_screen.png
│   │   ├── dashboard_admin.png
│   │   ├── modal_confirmacion.png
│   │   ├── auditoria_view.png
│   │   ├── mantenimiento_panel.png
│   │   ├── mobile_view.png
│   │   ├── export_excel.png
│   │   └── estados_confirmacion.png
│   ├── diagrams/
│   │   ├── use_case_general.png
│   │   ├── use_case_by_actor.png
│   │   ├── activity_confirmation.png
│   │   ├── class_diagram.png
│   │   ├── component_diagram.png
│   │   ├── er_diagram.png
│   │   └── database_schema.png
│   └── wireframes/
│       ├── login_wireframe.png
│       ├── dashboard_wireframe.png
│       └── mobile_wireframe.png
└── DOCUMENTACION_PROFESIONAL.md
```

#### Herramientas Recomendadas para Diagramas

**Para Diagramas UML:**
- **Lucidchart**: Diagramas profesionales en línea
- **Draw.io (diagrams.net)**: Gratuito y completo
- **PlantUML**: Diagramas como código
- **Visual Paradigm**: Herramienta profesional completa

**Para Diagramas de Base de Datos:**
- **MySQL Workbench**: Ingeniería reversa automática
- **dbdiagram.io**: Diagramas ER en línea
- **ERDPlus**: Herramienta académica gratuita

**Para Capturas de Pantalla:**
- **Snagit**: Herramienta profesional con anotaciones
- **Greenshot**: Gratuito y con edición básica
- **LightShot**: Capturas rápidas y simples

#### Estándares de Documentación Visual

**Resolución de Imágenes:**
- Capturas de pantalla: 1920x1080 mínimo
- Diagramas: 300 DPI para impresión
- Iconos: Formato vectorial (SVG) preferido

**Formato de Archivos:**
- Screenshots: PNG para calidad
- Diagramas: PNG o SVG
- Wireframes: PDF o PNG

**Convenciones de Nomenclatura:**
- `seccion_subseccion_nombre.extension`
- Ejemplo: `3_casosuso_diagrama_general.png`

### Anexo D: Estructura de Base de Datos Completa

[Diagrama ER detallado mostrando todas las relaciones entre tablas]

### Anexo D: APIs y Endpoints

#### Autenticación
- `POST /login` - Iniciar sesión
- `GET /logout` - Cerrar sesión

#### Registros
- `GET /auditoria` - Lista de registros
- `POST /auditoria/tabla` - Tabla paginada
- `POST /confirmar_redes/<id>` - Confirmar desde redes
- `POST /confirmar_gerencia/<id>` - Confirmar desde gerencia
- `POST /confirmar_redes_masivo` - Confirmación masiva redes
- `POST /confirmar_gerencia_masivo` - Confirmación masiva gerencia

#### Administración
- `GET /mantenimiento` - Panel de administración
- `POST /admin/usuarios` - Gestión de usuarios
- `POST /admin/editar_fecha_voucher` - Editar fecha comprobante
- `POST /admin/editar_fecha_ingreso` - Editar fecha ingreso

### Anexo E: Configuraciones de Entorno

#### Desarrollo
```env
FLASK_ENV=development
DEBUG=True
SECRET_KEY=dev_secret_key
DATABASE_URL=mysql://dev_user:dev_pass@localhost/gestion_caja_dev
```

#### Producción
```env
FLASK_ENV=production
DEBUG=False
SECRET_KEY=production_secret_key_very_long_and_secure
DATABASE_URL=mysql://prod_user:secure_pass@db_server/gestion_caja
```

### Anexo F: Scripts de Utilidad

#### Backup Automático
```bash
#!/bin/bash
# backup_database.sh
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups/gestion_caja"
mkdir -p $BACKUP_DIR

mysqldump -u $DB_USER -p$DB_PASS gestion_caja > \
  $BACKUP_DIR/backup_gestion_caja_$DATE.sql

# Comprimir backup
gzip $BACKUP_DIR/backup_gestion_caja_$DATE.sql

# Eliminar backups antiguos (más de 30 días)
find $BACKUP_DIR -name "*.sql.gz" -mtime +30 -delete
```

#### Verificación de Salud del Sistema
```python
#!/usr/bin/env python3
# health_check.py
import requests
import sys
import mysql.connector

def check_web_service():
    try:
        response = requests.get('http://localhost:5000/health', timeout=5)
        return response.status_code == 200
    except:
        return False

def check_database():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='app_caja',
            password='password',
            database='gestion_caja'
        )
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        conn.close()
        return True
    except:
        return False

if __name__ == "__main__":
    web_ok = check_web_service()
    db_ok = check_database()
    
    if web_ok and db_ok:
        print("Sistema operativo")
        sys.exit(0)
    else:
        print(f"Problemas detectados - Web: {web_ok}, DB: {db_ok}")
        sys.exit(1)
```

---

**FIN DE DOCUMENTACIÓN**

*Versión 1.0 - Agosto 2025*
*Desarrollado para Castillo de Chancay*
*Documento confidencial - Uso interno únicamente*
