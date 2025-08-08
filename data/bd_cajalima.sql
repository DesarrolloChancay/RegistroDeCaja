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
INSERT INTO registros_ventas (recibo, medio_pago_id, entidad_banco_id, area_id, centro_costo_id, detalle, empresa_id, monto, confirmado, fecha_registro_pago, fecha_comprobante, fecha_ingreso_cuenta, fecha_confirmacion_redes, fecha_confirmacion_gerencia, confirmado_redes, vendedor_id, confirmado_por_gerencia, confirmado_por_redes) VALUES
('REC001', 7, 1, 1, 1, 'Venta de habitación Deluxe', 1, 450.00, 1, '2024-05-01', '2024-05-01', '2024-05-02', '2024-05-02 10:00:00', '2024-05-03 11:30:00', FALSE,  'vend01', 'admin01', 'verif01'),
('REC002', 2, NULL, 3, 3, 'Venta de servicio de consultoría', 1, 150.50, 0, '2024-05-02', '2024-05-02', NULL, NULL, NULL, FALSE, 'vend02', NULL, NULL),
('REC003', 3, 2, 1, 1, 'Venta de 5 noches en suite', 1, 1200.75, 1, '2024-05-03', '2024-05-03', '2024-05-04', '2024-05-03 16:20:00', '2024-05-04 10:00:00', TRUE, 'vend01', 'admin01', 'verif01'),
('REC004', 1, NULL, 2, 2, 'Venta a grupo corporativo A', 1, 3500.00, 0, '2024-05-04', '2024-05-04', NULL, '2024-05-04 18:00:00', NULL, FALSE, 'vend02', NULL, 'verif01'),
('REC005', 6, 3, 1, 1, 'Depósito por reserva de evento', 1, 800.00, 1, '2024-05-05', '2024-05-05', '2024-05-06', '2024-05-05 14:00:00', '2024-05-07 09:00:00', FALSE, 'vend01', 'admin01', 'verif01'),
('REC006', 4, NULL, 3, 3, 'Venta de software', 1, 250.00, 0, '2024-05-06', '2024-05-06', NULL, NULL, NULL, FALSE, 'vend02', NULL, NULL),
('REC007', 7, 4, 1, 1, 'Transferencia por servicio de spa', 1, 180.25, 1, '2024-05-07', '2024-05-07', '2024-05-07', '2024-05-07 11:00:00', '2024-05-08 10:30:00', TRUE, 'vend01', 'admin01', 'verif01'),
('REC008', 3, 1, 2, 2, 'Servicios para conferencia', 1, 5500.00, 1, '2024-05-08', '2024-05-08', '2024-05-09', '2024-05-08 17:00:00', '2024-05-09 12:00:00', TRUE, 'vend02', 'admin01', 'verif01'),
('REC009', 2, NULL, 1, 1, 'Venta de productos de la tienda', 1, 75.00, 0, '2024-05-09', '2024-05-09', NULL, NULL, NULL, FALSE, 'vend01', NULL, NULL),
('REC010', 5, NULL, 3, 3, 'Pago de factura pendiente', 1, 320.00, 1, '2024-05-10', '2024-05-10', '2024-05-10', '2024-05-10 13:00:00', '2024-05-11 09:15:00', TRUE, 'vend02', 'admin01', 'verif01'),
('REC011', 1, NULL, 1, 1, 'Pago por servicios de lavandería', 1, 45.00, 0, '2024-05-11', '2024-05-11', NULL, NULL, NULL, FALSE, 'vend01', NULL, NULL),
('REC012', 6, 2, 2, 2, 'Depósito de cliente B', 1, 950.00, 1, '2024-05-12', '2024-05-12', '2024-05-13', '2024-05-13 10:00:00', '2024-05-14 11:00:00', FALSE, 'vend02', 'admin01', 'verif01'),
('REC013', 7, 3, 3, 3, 'Pago por servicios de diseño web', 1, 600.00, 0, '2024-05-13', '2024-05-13', NULL, NULL, NULL, FALSE, 'vend01', NULL, NULL),
('REC014', 3, 4, 1, 1, 'Venta de desayuno buffet', 1, 120.00, 1, '2024-05-14', '2024-05-14', '2024-05-15', '2024-05-14 10:00:00', '2024-05-15 10:00:00', TRUE, 'vend02', 'admin01', 'verif01'),
('REC015', 8, NULL, 2, 2, 'Otros ingresos', 1, 25.00, 0, '2024-05-15', '2024-05-15', NULL, '2024-05-15 12:00:00', NULL, TRUE, 'vend01', NULL, 'verif01');


SELECT * FROM registros_ventas