# Documentación Técnica del Proyecto: Registro de Caja

## 1. Descripción General

Registro de Caja es una aplicación web desarrollada en Flask para la gestión y auditoría de registros de caja, con control de acceso por roles (admin, verificador, vendedor), confirmaciones de transacciones y administración de usuarios y ventas.

---

## 2. Estructura de Carpetas y Archivos

```
RegistroDeCaja/
│
├── app/
│   ├── __init__.py           # Inicialización de la app Flask, registro de blueprints, configuración de rutas principales y login
│   ├── config.py             # Configuración de Flask (variables de entorno, conexión BD, claves secretas)
│   ├── extensions.py         # Inicialización de db (SQLAlchemy) y login_manager (Flask-Login)
│   ├── models/
│   │   ├── Usuario.py        # Modelo de usuario y roles (hereda de db.Model y UserMixin)
│   │   ├── registro_venta.py # Modelo de registro de ventas (campos de auditoría y confirmaciones)
│   │   ├── admin.py          # Modelo de superusuario admin
│   ├── controllers/
│   │   ├── auditoria_controller.py # Lógica de negocio para auditoría, helpers y utilidades
│   │   ├── admin_controller.py     # Lógica exclusiva para admin (gestión de usuarios, mantenimiento)
│   ├── routes/
│   │   ├── auditoria_routes.py     # Rutas de auditoría y confirmaciones (GET/POST, AJAX)
│   │   ├── admin_routes.py         # Rutas exclusivas para admin
│   ├── templates/
│   │   ├── base.html               # Template base, navegación y layout
│   │   ├── login.html              # Login de usuario
│   │   ├── auditoria/
│   │   │   ├── auditoria.html      # Vista principal de auditoría
│   │   │   └── _tabla_auditoria.html # Partial de la tabla de auditoría (AJAX)
│   │   └── admin/
│   │       └── mantenimiento.html  # Vista exclusiva admin para mantenimiento
│   ├── static/
│       ├── js/app.js               # Lógica JS para confirmaciones, AJAX, paginación y exportación
│       └── ...
├── data/
│   └── bd_cajalima.sql            # Script de creación y datos de la BD (roles, usuarios, ventas)
├── run.py                         # Arranque de la app Flask
├── requirements.txt               # Dependencias y librerías del proyecto
├── DOCUMENTACION.md               # Este archivo
└── README.md
```
