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
    recibo VARCHAR(100) UNIQUE,
    medio_pago_id INT,
    entidad_banco_id INT,
    area_id INT,
    centro_costo_id INT,
    detalle TEXT,
    empresa_id INT,
    monto DECIMAL(10,2),
    confirmado BOOLEAN DEFAULT 0,
    fecha_registro_pago DATE, -- Va a venir de sistema Xafiro
    fecha_comprobante DATE, -- Es la fecha que ingresa redes del comprobante
    fecha_ingreso_cuenta DATE, -- Fecha que corrobora gerencia de cuando entró el pago a la cuenta
    fecha_confirmacion_redes DATETIME, -- Fecha automatica que guarda cuando se confirma por redes
    fecha_confirmacion_gerencia DATETIME, -- Fecha automatica que guarda cuando se confirma por gerencia
    confirmado_redes BOOLEAN DEFAULT 0,
    vendedor_id VARCHAR(100),
    confirmado_por_gerencia VARCHAR(100),
    confirmado_por_redes VARCHAR(100),

    FOREIGN KEY (empresa_id) REFERENCES empresas(id),
    FOREIGN KEY (area_id) REFERENCES areas(id),
    FOREIGN KEY (medio_pago_id) REFERENCES medios_pago(id),
    FOREIGN KEY (entidad_banco_id) REFERENCES entidades_banco(id),
    FOREIGN KEY (centro_costo_id) REFERENCES centros_costo(id),
    FOREIGN KEY (vendedor_id) REFERENCES usuarios(id),
    FOREIGN KEY (confirmado_por_gerencia) REFERENCES usuarios(id),
    FOREIGN KEY (confirmado_por_redes) REFERENCES usuarios(id)
);


-- --- Inserción de datos ---

-- Insertar roles
INSERT INTO roles (nombre) VALUES
('admin'),
('vendedor'),
('verificador');

-- Insertar empresas
INSERT INTO empresas (nombre) VALUES
('Resource');

-- Insertar áreas
INSERT INTO areas (nombre) VALUES
('HOTEL'),
('GRUPOS COORPORATIVOS'),
('COMERCIAL');

-- Insertar entidades bancarias
INSERT INTO entidades_banco (nombre) VALUES
('BCP'),
('BBVA'),
('Scotiabank'),
('Interbank');

-- Insertar medios de pago
INSERT INTO medios_pago (nombre) VALUES
('EFECTIVO'),
('POS - YAPE'),
('POS - TARJETA'),
('POS - PLIN'),
('PAGOLINK'),
('DEPOSITO'),
('TRANSFERENCIA'),
('OTROS');

-- Insertar centros de costo
INSERT INTO centros_costo (nombre) VALUES
('Caja - Hotel'),
('Caja - Redes'),
('Caja - Comercial');

-- Insertar usuarios
INSERT INTO usuarios (id, nombre, correo, contrasena, rol_id) VALUES
('admin01', 'Admin General', 'admin@resource.com', 'admin123', 1),
('vend01', 'Lucía Vendedora', 'lucia@resource.com', 'vend123', 2),
('vend02', 'Pedro Vendedor', 'pedro@resource.com', 'vend123', 2),
('verif01', 'Sandra Verificadora', 'sandra@resource.com', 'verif123', 3);

-- Insertar registros de ventas
INSERT INTO registros_ventas (
    fecha_registro, recibo, medio_pago_id, entidad_banco_id, area_id, centro_costo_id,
    detalle, empresa_id, monto, confirmado_general, fecha_ingreso_cuenta, confirmado_por_redes,
    fecha_confirmacion_redes, vendedor_id, verificador_gerencia_id, verificador_redes_id,
    confirmado_por_gerencia
) VALUES
('2025-08-01', 'RC001', 1, 1, 1, 1, 'Reserva habitación sencilla', 1, 250.00, TRUE, '2025-08-02', TRUE, '2025-08-02 10:00:00', 'vend01', 'admin01', 'verif01', TRUE),
('2025-08-01', 'RC002', 2, 1, 1, 1, 'Pago con YAPE por habitación doble', 1, 300.00, TRUE, '2025-08-02', TRUE, '2025-08-02 11:30:00', 'vend02', 'admin01', 'verif01', TRUE),
('2025-08-02', 'RC003', 3, 2, 2, 2, 'Pago por evento empresarial', 1, 1200.00, TRUE, '2025-08-03', TRUE, '2025-08-03 09:00:00', 'vend01', 'admin01', 'verif01', TRUE),
('2025-08-02', 'RC004', 4, 2, 2, 3, 'Pago con PLIN por grupo', 1, 800.00, FALSE, NULL, FALSE, NULL, 'vend02', 'admin01', NULL, FALSE),
('2025-08-03', 'RC005', 5, 3, 1, 1, 'Pago con link por habitación', 1, 500.00, FALSE, NULL, FALSE, NULL, 'vend01', NULL, NULL, FALSE),
('2025-08-03', 'RC006', 6, 1, 1, 1, 'Depósito por servicios adicionales', 1, 200.00, TRUE, '2025-08-04', FALSE, NULL, 'vend02', 'admin01', NULL, TRUE),
('2025-08-04', 'RC007', 7, 2, 2, 2, 'Transferencia por convención', 1, 1800.00, TRUE, '2025-08-05', TRUE, '2025-08-05 14:00:00', 'vend01', 'admin01', 'verif01', TRUE),
('2025-08-04', 'RC008', 8, 3, 1, 3, 'Otros medios por reserva corporativa', 1, 950.00, FALSE, NULL, FALSE, NULL, 'vend02', NULL, NULL, FALSE),
('2025-08-05', 'RC009', 1, 1, 1, 1, 'Efectivo por habitación ejecutiva', 1, 650.00, TRUE, '2025-08-05', TRUE, '2025-08-05 16:00:00', 'vend01', 'admin01', 'verif01', TRUE),
('2025-08-05', 'RC010', 2, 2, 2, 3, 'Pago YAPE por grupo empresarial', 1, 1350.00, FALSE, NULL, FALSE, NULL, 'vend02', NULL, NULL, FALSE),
('2025-08-06', 'RC011', 7, 4, 1, 1, 'Transferencia Interbank por reserva suite', 1, 750.00, TRUE, '2025-08-06', TRUE, '2025-08-06 10:15:00', 'vend01', 'admin01', 'verif01', TRUE),
('2025-08-06', 'RC012', 3, 2, 2, 2, 'Pago con tarjeta por catering', 1, 550.00, TRUE, '2025-08-06', TRUE, '2025-08-06 11:45:00', 'vend02', 'admin01', 'verif01', TRUE),
('2025-08-07', 'RC013', 1, 1, 3, 3, 'Efectivo por servicio de mensajería', 1, 150.00, FALSE, NULL, FALSE, NULL, 'vend01', NULL, NULL, FALSE),
('2025-08-07', 'RC014', 5, 3, 1, 1, 'Pago con link por habitación familiar', 1, 450.00, FALSE, NULL, FALSE, NULL, 'vend02', NULL, NULL, FALSE),
('2025-08-08', 'RC015', 6, 4, 2, 2, 'Depósito en Scotiabank por alquiler de sala', 1, 1500.00, TRUE, '2025-08-08', TRUE, '2025-08-08 15:30:00', 'vend01', 'admin01', 'verif01', TRUE);
