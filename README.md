# Documentación Técnica del Proyecto: Registro de Caja

## 1. Descripción General

Registro de Caja es una aplicación web desarrollada en Flask para la gestión y auditoría de registros de caja, con control de acceso por roles (admin, verificador, vendedor, contabilidad), confirmaciones de transacciones y administración de usuarios y ventas.

## 2. Estructura de Carpetas y Archivos

```plaintext
RegistroDeCaja/
│
├── app/                       # Directorio principal de la aplicación
│   ├── __init__.py           # Inicialización de Flask y blueprints
│   ├── config.py             # Configuración de entornos y variables
│   ├── extensions.py         # SQLAlchemy y Flask-Login
│   │
│   ├── models/               # Modelos de datos
│   │   ├── __init__.py
│   │   ├── Usuario.py        # Modelo de usuarios y roles
│   │   ├── registro_venta.py # Modelo de registros y auditoría
│   │   └── admin.py          # Modelo de administración
│   │
│   ├── controllers/          # Lógica de negocio
│   │   ├── __init__.py
│   │   ├── auditoria_controller.py  # Control de registros
│   │   └── admin_controller.py      # Gestión administrativa
│   │
│   ├── routes/              # Definición de rutas
│   │   ├── __init__.py
│   │   ├── auditoria_routes.py # Endpoints de auditoría
│   │   └── admin_routes.py     # Endpoints administrativos
│   │
│   ├── forms/              # Formularios y validaciones
│   │   └── __init__.py
│   │
│   ├── services/           # Servicios adicionales
│   │   └── __init__.py
│   │
│   ├── templates/          # Plantillas HTML
│   │   ├── base.html      # Template base con navegación
│   │   ├── login.html     # Página de inicio de sesión
│   │   ├── 403.html       # Página de acceso denegado
│   │   ├── 404.html       # Página no encontrada
│   │   ├── auditoria/     # Vistas de auditoría
│   │   │   ├── auditoria.html
│   │   │   └── _tabla_auditoria.html
│   │   └── admin/         # Vistas administrativas
│   │       ├── mantenimiento.html
│   │       ├── registrosauditoria.html
│   │       ├── _tabla_generica.html
│   │       └── _tabla_registrosauditoria.html
│   │
│   └── static/            # Recursos estáticos
│       ├── css/           # Estilos Tailwind y personalizados
│       ├── js/            # Scripts JavaScript
│       │   ├── app.js     # Lógica principal y auditoría
│       │   ├── admin.js   # Funciones administrativas
│       │   └── security.min.js # Seguridad y control de sesiones
│       └── img/           # Imágenes y logos
│           ├── castillo.svg
│           ├── logo.svg
│           ├── logout.svg
│           ├── escudo_denegado.svg
│           └── cropped-CASTILLO-DE-CHANCAY-*.png
│
├── data/                  # Datos y scripts
│   └── bd_cajalima.sql   # Script de base de datos
│
├── .gitignore            # Configuración de Git
├── README.md             # Esta documentación
├── requirements.txt      # Dependencias del proyecto
└── run.py               # Punto de entrada de la aplicación
```


## 3. Características Principales

- **Sistema de Autenticación y Roles**:
  - Admin: Acceso total, gestión de usuarios y registros
  - Verificador: Confirmación de ingresos a cuenta
  - Vendedor: Confirmación de comprobantes y vouchers
  - Contabilidad: Visualización de registros

- **Gestión de Registros**:
  - Confirmación individual y masiva de registros
  - Validación de fechas y horas
  - Sistema de auditoría completo
  - Exportación de datos

- **Seguridad**:
  - Sesiones con tiempo de inactividad
  - Registro de acciones de usuarios
  - Validación de permisos por rol
  - Protección contra CSRF

- **Interfaz**:
  - Diseño responsivo con Tailwind CSS
  - Actualizaciones en tiempo real con AJAX
  - Filtros y búsqueda dinámica
  - Paginación avanzada

## 4. Requisitos del Sistema

- Python 3.10 o superior
- MySQL/MariaDB
- Navegador web moderno
- Git (para clonar el repositorio)

## 5. Instalación y Configuración

1. **Clonar el Repositorio**:
   ```bash
   git clone https://github.com/DesarrolloChancay/RegistroDeCaja.git
   cd RegistroDeCaja
   ```

2. **Crear y Activar Entorno Virtual**:
   ```bash
   python -m venv venv
   # En Windows:
   venv\Scripts\activate
   # En Linux/Mac:
   source venv/bin/activate
   ```

3. **Instalar Dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar Base de Datos**:
   - Crear una base de datos MySQL
   - Importar el esquema desde `data/bd_cajalima.sql`
   - Configurar las credenciales en `app/config.py`

5. **Variables de Entorno**:
   Crear archivo `.env` en la raíz del proyecto:
   ```env
   FLASK_APP=run.py
   FLASK_ENV=development
   SECRET_KEY=tu_clave_secreta
   DATABASE_URL=mysql://usuario:contraseña@localhost/bd_cajalima
   ```

6. **Iniciar la Aplicación**:
   ```bash
   flask run
   ```
   La aplicación estará disponible en `http://localhost:5000`