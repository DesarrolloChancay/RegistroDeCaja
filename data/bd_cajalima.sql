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
    session_active BOOLEAN DEFAULT 0, -- para saber si está activo en la sesión
    FOREIGN KEY (rol_id) REFERENCES roles(id)
);

-- Tabla principal de registros de ventas
CREATE TABLE registros_ventas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_xafiro INT UNIQUE, -- ID único de Xafiro
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
    fecha_comprobante DATE, -- Fecha que ingresa redes del comprobante
    fecha_ingreso_cuenta DATE, -- Fecha que corrobora gerencia de cuando entró el pago a la cuenta
    fecha_confirmacion_redes DATETIME, -- Fecha automática cuando se confirma por redes
    fecha_confirmacion_gerencia DATETIME, -- Fecha automática cuando se confirma por gerencia
    confirmado_redes BOOLEAN DEFAULT 0,
    vendedor_id VARCHAR(100), -- (si luego decides eliminarla, hazlo con ALTER)
    confirmador_voucher VARCHAR(100), -- quien confirma comprobante (redes)
    confirmador_cuenta  VARCHAR(100), -- quien confirma ingreso a cuenta (gerencia)

    FOREIGN KEY (empresa_id) REFERENCES empresas(id),
    FOREIGN KEY (area_id) REFERENCES areas(id),
    FOREIGN KEY (medio_pago_id) REFERENCES medios_pago(id),
    FOREIGN KEY (entidad_banco_id) REFERENCES entidades_banco(id),
    FOREIGN KEY (centro_costo_id) REFERENCES centros_costo(id),
    FOREIGN KEY (confirmador_cuenta) REFERENCES usuarios(id),
    FOREIGN KEY (confirmador_voucher) REFERENCES usuarios(id)
);

-- Jesus estoy creando esta tabla nueva para auditar los cambios ( he tratado de que no afecte lo avanzado )
CREATE TABLE auditoria_registros_ventas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    registro_venta_id INT NOT NULL,
    usuario_id VARCHAR(100) NOT NULL,
    accion ENUM('INSERT', 'UPDATE', 'DELETE') NOT NULL,
    campo_modificado VARCHAR(100), -- nombre del campo que cambió
    valor_anterior TEXT, -- valor antes del cambio
    valor_nuevo TEXT, -- valor después del cambio
    fecha_cambio DATETIME DEFAULT CURRENT_TIMESTAMP,
    motivo_cambio TEXT, -- opcional: razón del cambio
    ip_usuario VARCHAR(45), -- Vamos a guardar también esto: el IP desde donde se hizo el cambio
    FOREIGN KEY (registro_venta_id) REFERENCES registros_ventas(id),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    INDEX idx_registro_fecha (registro_venta_id, fecha_cambio)
);

-- --- Inserción de datos ---

-- Insertar roles
INSERT INTO roles (nombre) VALUES
('admin'),
('vendedor'),
('verificador'),
('contabilidad');

-- Crear usuario SISTEMA para auditoría automática sin contexto
INSERT INTO usuarios (id, nombre, correo, contrasena, rol_id) VALUES
('SYSTEM', 'Sistema', 'sistema@castillodechancay.com', '$2b$12$GF3wych4N14sa/WBzxyoH.MxcCD5ruIsFNVn2UUR73S.JK0ATLkZC', 1)
ON DUPLICATE KEY UPDATE nombre=VALUES(nombre);

-- Insertar empresas
INSERT INTO empresas (nombre) VALUES
('RESORT');

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
('admin01', 'Alfredo Huaman', 'estadistica@castillodechancay.com', '$2b$12$jeZG0C.IXQsL/zmrvCS/4OBnfPIHDdDQs2KrdqUWVUqPnXPdTeyte', 1),
('vend01', 'Sebastian Moran', 'ventas@castillodechancay.com', '$2b$12$3yXJSC8hk9.yr46fsUdjs.IH4clkB1311UTgHzWMd.tX.iS1BuNJW', 2),
('vend02', 'Estefany Aguirre', 'redes@castillodechancay.com', '$2b$12$MiwMi8t.URMdCr3cdD9wceCtK5bnkUkkiGLxg/GP2GMWlt1NOXx6.', 2),
('vend03', 'Elias Sanchez', 'ventas2@castillodechancay.com', '$2b$12$VzyVakHHzTeaynbFsCkeaObdl29CceeV4FnTEg8hbFbBepNzQNENy', 2),
('verif01', 'Ana Zavala', 'asistente.gerencia.lima@castillodechancay.com', '$2b$12$vXn/LKmrYSyB50ex202nSuBvfATlroXWtLNMEEjXBZ5XhndTNDBi2', 3),
('verif02', 'Yolanda Pacheco', 'gerenciacastillochancay@hotmail.com', '$2b$12$k2yfxjtEGCqcZ3mriHfeUe7lLSHbfS6mOQRkDCwyC0khQ3uhd/G9.', 3)
ON DUPLICATE KEY UPDATE nombre=VALUES(nombre);

-- Insertar registros de ventas (ejemplos)
INSERT INTO registros_ventas (
    recibo,
    medio_pago_id,
    entidad_banco_id,
    area_id,
    centro_costo_id,
    detalle,
    empresa_id,
    monto,
    confirmado,
    fecha_registro_pago,
    fecha_comprobante,
    fecha_ingreso_cuenta,
    fecha_confirmacion_redes,
    fecha_confirmacion_gerencia,
    confirmado_redes,
    vendedor_id,
    confirmador_cuenta,
    confirmador_voucher
) VALUES
(0001, 'REC001', 7, 1, 1, 1, 'Venta de habitación Deluxe', 1, 450.00, 0, '2025-08-01', NULL, NULL, NULL, NULL, 0, NULL, NULL, NULL),
(0002, 'REC002', 2, 3, 3, 3, 'Venta de servicio de consultoría', 1, 150.50, 0, '2025-08-02', NULL, NULL, NULL, NULL, 0, NULL, NULL, NULL),
(0003, 'REC003', 3, 2, 1, 1, 'Venta de 5 noches en suite', 1, 1200.75, 0, '2025-08-03', NULL, NULL, NULL, NULL, 0, NULL, NULL, NULL),
(0004, 'REC004', 1, 2, 2, 2, 'Venta a grupo corporativo A', 1, 3500.00, 0, '2025-08-04', NULL, NULL, NULL, NULL, 0, NULL, NULL, NULL),
(0005, 'REC005', 6, 3, 1, 1, 'Depósito por reserva de evento', 1, 800.00, 0, '2025-08-05', NULL, NULL, NULL, NULL, 0, NULL, NULL, NULL),
(0006, 'REC006', 4, 4, 3, 3, 'Venta de software', 1, 250.00, 0, '2025-08-06', NULL, NULL, NULL, NULL, 0, NULL, NULL, NULL),
(0007, 'REC007', 7, 4, 1, 1, 'Transferencia por servicio de spa', 1, 180.25, 0, '2025-08-07', NULL, NULL, NULL, NULL, 0, NULL, NULL, NULL),
(0008, 'REC008', 3, 1, 2, 2, 'Servicios para conferencia', 1, 5500.00, 0, '2025-08-08', NULL, NULL, NULL, NULL, 0, NULL, NULL, NULL),
(0009, 'REC009', 2, 2, 1, 1, 'Venta de productos de la tienda', 1, 75.00, 0, '2025-08-09', NULL, NULL, NULL, NULL, 0, NULL, NULL, NULL),
(0010, 'REC010', 5, 3, 3, 3, 'Pago de factura pendiente', 1, 320.00, 0, '2025-08-10', NULL, NULL, NULL, NULL, 0, NULL, NULL, NULL),
(0011, 'REC011', 1, 1, 1, 1, 'Pago por servicios de lavandería', 1, 45.00, 0, '2025-08-11', NULL, NULL, NULL, NULL, 0, NULL, NULL, NULL),
(0012, 'REC012', 6, 2, 2, 2, 'Depósito de cliente B', 1, 950.00, 0, '2025-08-12', NULL, NULL, NULL, NULL, 0, NULL, NULL, NULL),
(0013, 'REC013', 7, 3, 3, 3, 'Pago por servicios de diseño web', 1, 600.00, 0, '2025-08-13', NULL, NULL, NULL, NULL, 0, NULL, NULL, NULL),
(0014, 'REC014', 3, 4, 1, 1, 'Venta de desayuno buffet', 1, 120.00, 0, '2025-08-14', NULL, NULL, NULL, NULL, 0, NULL, NULL, NULL),
(0015, 'REC015', 8, 1, 2, 2, 'Otros ingresos', 1, 25.00, 0, '2025-08-15', NULL, NULL, NULL, NULL, 0, NULL, NULL, NULL);




-- Variables de sesión para el contexto de auditoría, mira esto lo agrego para setear estas variables en un inicio
SET @current_user_id = NULL;
SET @change_reason   = NULL;
SET @user_ip         = NULL;

-- TRIGGERS PARA AUDITORÍA AUTOMÁTICA
DELIMITER $$

-- TRIGGER PARA el INSERT
CREATE TRIGGER tr_registros_ventas_insert
AFTER INSERT ON registros_ventas
FOR EACH ROW
BEGIN
    INSERT INTO auditoria_registros_ventas (
        registro_venta_id, usuario_id, accion, campo_modificado,
        valor_anterior, valor_nuevo, motivo_cambio, ip_usuario
    ) VALUES (
        NEW.id,
        COALESCE(@current_user_id, 'SYSTEM'),
        'INSERT',
        'REGISTRO_COMPLETO',
        NULL,
        CONCAT('recibo:', IFNULL(NEW.recibo, 'NULL'),
               '; monto:', IFNULL(NEW.monto, 'NULL'),
               '; empresa_id:', IFNULL(NEW.empresa_id, 'NULL')),
        @change_reason,
        @user_ip
    );
END$$


-- TRIGGER PARA el UPDATE

CREATE TRIGGER tr_registros_ventas_update 
AFTER UPDATE ON registros_ventas
FOR EACH ROW
BEGIN
    -- Helper para comparar NULL-safe: NOT (OLD <=> NEW) detecta cambios incluyendo NULL
    -- recibo
    IF NOT (OLD.recibo <=> NEW.recibo) THEN
        INSERT INTO auditoria_registros_ventas
        (registro_venta_id, usuario_id, accion, campo_modificado, valor_anterior, valor_nuevo, motivo_cambio, ip_usuario)
        VALUES (NEW.id, COALESCE(@current_user_id, 'SYSTEM'), 'UPDATE', 'recibo', OLD.recibo, NEW.recibo, @change_reason, @user_ip);
    END IF;

    -- monto
    IF NOT (OLD.monto <=> NEW.monto) THEN
        INSERT INTO auditoria_registros_ventas
        (registro_venta_id, usuario_id, accion, campo_modificado, valor_anterior, valor_nuevo, motivo_cambio, ip_usuario)
        VALUES (NEW.id, COALESCE(@current_user_id, 'SYSTEM'), 'UPDATE', 'monto', OLD.monto, NEW.monto, @change_reason, @user_ip);
    END IF;

    -- fecha_comprobante
    IF NOT (OLD.fecha_comprobante <=> NEW.fecha_comprobante) THEN
        INSERT INTO auditoria_registros_ventas
        (registro_venta_id, usuario_id, accion, campo_modificado, valor_anterior, valor_nuevo, motivo_cambio, ip_usuario)
        VALUES (NEW.id, COALESCE(@current_user_id, 'SYSTEM'), 'UPDATE', 'fecha_comprobante', OLD.fecha_comprobante, NEW.fecha_comprobante, @change_reason, @user_ip);
    END IF;

    -- fecha_ingreso_cuenta
    IF NOT (OLD.fecha_ingreso_cuenta <=> NEW.fecha_ingreso_cuenta) THEN
        INSERT INTO auditoria_registros_ventas
        (registro_venta_id, usuario_id, accion, campo_modificado, valor_anterior, valor_nuevo, motivo_cambio, ip_usuario)
        VALUES (NEW.id, COALESCE(@current_user_id, 'SYSTEM'), 'UPDATE', 'fecha_ingreso_cuenta', OLD.fecha_ingreso_cuenta, NEW.fecha_ingreso_cuenta, @change_reason, @user_ip);
    END IF;

    -- confirmado_redes
    IF NOT (OLD.confirmado_redes <=> NEW.confirmado_redes) THEN
        INSERT INTO auditoria_registros_ventas
        (registro_venta_id, usuario_id, accion, campo_modificado, valor_anterior, valor_nuevo, motivo_cambio, ip_usuario)
        VALUES (NEW.id, COALESCE(@current_user_id, 'SYSTEM'), 'UPDATE', 'confirmado_redes', OLD.confirmado_redes, NEW.confirmado_redes, @change_reason, @user_ip);
    END IF;

    -- confirmado (gerencia)
    IF NOT (OLD.confirmado <=> NEW.confirmado) THEN
        INSERT INTO auditoria_registros_ventas
        (registro_venta_id, usuario_id, accion, campo_modificado, valor_anterior, valor_nuevo, motivo_cambio, ip_usuario)
        VALUES (NEW.id, COALESCE(@current_user_id, 'SYSTEM'), 'UPDATE', 'confirmado', OLD.confirmado, NEW.confirmado, @change_reason, @user_ip);
    END IF;

    -- confirmador_voucher (antes: confirmador_voucher)
    IF NOT (OLD.confirmador_voucher <=> NEW.confirmador_voucher) THEN
        INSERT INTO auditoria_registros_ventas
        (registro_venta_id, usuario_id, accion, campo_modificado, valor_anterior, valor_nuevo, motivo_cambio, ip_usuario)
        VALUES (NEW.id, COALESCE(@current_user_id, 'SYSTEM'), 'UPDATE', 'confirmador_voucher', OLD.confirmador_voucher, NEW.confirmador_voucher, @change_reason, @user_ip);
    END IF;

    -- confirmador_cuenta (antes: confirmador_cuenta)
    IF NOT (OLD.confirmador_cuenta <=> NEW.confirmador_cuenta) THEN
        INSERT INTO auditoria_registros_ventas
        (registro_venta_id, usuario_id, accion, campo_modificado, valor_anterior, valor_nuevo, motivo_cambio, ip_usuario)
        VALUES (NEW.id, COALESCE(@current_user_id, 'SYSTEM'), 'UPDATE', 'confirmador_cuenta', OLD.confirmador_cuenta, NEW.confirmador_cuenta, @change_reason, @user_ip);
    END IF;

    -- detalle
    IF NOT (OLD.detalle <=> NEW.detalle) THEN
        INSERT INTO auditoria_registros_ventas
        (registro_venta_id, usuario_id, accion, campo_modificado, valor_anterior, valor_nuevo, motivo_cambio, ip_usuario)
        VALUES (NEW.id, COALESCE(@current_user_id, 'SYSTEM'), 'UPDATE', 'detalle', OLD.detalle, NEW.detalle, @change_reason, @user_ip);
    END IF;

END$$

-- TRIGGER PARA DELETE
CREATE TRIGGER tr_registros_ventas_delete 
BEFORE DELETE ON registros_ventas
FOR EACH ROW
BEGIN
    INSERT INTO auditoria_registros_ventas (
        registro_venta_id, usuario_id, accion, campo_modificado,
        valor_anterior, valor_nuevo, motivo_cambio, ip_usuario
    ) VALUES (
        OLD.id,
        COALESCE(@current_user_id, 'SYSTEM'),
        'DELETE',
        'REGISTRO_COMPLETO',
        CONCAT('recibo:', IFNULL(OLD.recibo, 'NULL'),
               '; monto:', IFNULL(OLD.monto, 'NULL'),
               '; empresa_id:', IFNULL(OLD.empresa_id, 'NULL')),
        NULL,
        @change_reason,
        @user_ip
    );
END$$

DELIMITER ;

-- store procedure para manejar el contexto de auditoría ( el seteo y la limpieza )
DELIMITER $$

CREATE PROCEDURE SetAuditContext(
    IN p_user_id VARCHAR(100),
    IN p_reason TEXT,
    IN p_ip VARCHAR(45)
)
BEGIN
    SET @current_user_id = p_user_id;
    SET @change_reason   = p_reason;
    SET @user_ip         = p_ip;
END$$

CREATE PROCEDURE ClearAuditContext()
BEGIN
    SET @current_user_id = NULL;
    SET @change_reason   = NULL;
    SET @user_ip         = NULL;
END$$

DELIMITER ;

-- Aquí te agrego una vista, nos servirá para ver la auditoría de forma más easy xd
CREATE OR REPLACE VIEW v_auditoria_registros AS
SELECT 
    a.id,
    a.registro_venta_id,
    r.recibo,
    u.nombre AS usuario_nombre,
    u.correo AS usuario_correo,
    a.accion,
    a.campo_modificado,
    a.valor_anterior,
    a.valor_nuevo,
    a.fecha_cambio,
    a.motivo_cambio,
    a.ip_usuario
FROM auditoria_registros_ventas a
LEFT JOIN registros_ventas r ON a.registro_venta_id = r.id
LEFT JOIN usuarios u ON a.usuario_id = u.id
ORDER BY a.fecha_cambio DESC;

-- Consulta final para verificar datos
SELECT * FROM registros_ventas;