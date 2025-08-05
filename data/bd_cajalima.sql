-- Crear la base de datos
CREATE DATABASE IF NOT EXISTS gestion_caja;
USE gestion_caja;

-- Tabla de roles (admin, vendedor, gerencia, etc.)
CREATE TABLE roles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) UNIQUE NOT NULL
);

-- Tabla de empresas o clientes
CREATE TABLE empresas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL UNIQUE
);

-- Tabla de áreas (ej: Boletería, Comercial, etc.)
CREATE TABLE areas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL UNIQUE
);

-- Tabla de entidad_bancos
CREATE TABLE entidades_banco (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL UNIQUE
);

-- Tabla de medio de pago
CREATE TABLE medios_pago (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL UNIQUE
);

-- Tabla de centros de costo
CREATE TABLE centros_costo (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL UNIQUE
);

-- Tabla de usuarios
CREATE TABLE usuarios (
    id VARCHAR(100) PRIMARY KEY, -- puede ser UID o correo
    nombre VARCHAR(255) NOT NULL,
    correo VARCHAR(255) UNIQUE NOT NULL,
    contrasena VARCHAR(255) NOT NULL,
    rol_id INT NOT NULL,
    FOREIGN KEY (rol_id) REFERENCES roles(id)
);

-- Tabla principal de registros de ventas
CREATE TABLE registros_ventas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fecha_comprobante DATE,
    recibo VARCHAR(100) UNIQUE,
    medio_pago_id INT,
    entidad_banco_id INT,
    area_id INT,
    centro_costo_id INT,
    detalle TEXT,
    empresa_id INT,
    monto DECIMAL(10,2),
    confirmado BOOLEAN DEFAULT 0,
    fecha_pago_recibido DATE,
    confirmado_redes BOOLEAN DEFAULT 0,
    fecha_confirmacion_redes DATE,
    vendedor_id VARCHAR(100),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    confirmado_por_gerencia VARCHAR(100),
    confirmado_por_redes VARCHAR(100),
    fecha_confirmacion DATE,

    FOREIGN KEY (empresa_id) REFERENCES empresas(id),
    FOREIGN KEY (area_id) REFERENCES areas(id),
    FOREIGN KEY (medio_pago_id) REFERENCES medios_pago(id),
    FOREIGN KEY (entidad_banco_id) REFERENCES entidades_banco(id),
    FOREIGN KEY (centro_costo_id) REFERENCES centros_costo(id),
    FOREIGN KEY (vendedor_id) REFERENCES usuarios(id),
    FOREIGN KEY (confirmado_por_gerencia) REFERENCES usuarios(id),
    FOREIGN KEY (confirmado_por_redes) REFERENCES usuarios(id)
);
