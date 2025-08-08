# Archivo: app/models/registro_venta.py
# Se han ajustado los tipos de datos para las fechas de confirmación.

from app.extensions import db
from datetime import datetime

class RegistroVenta(db.Model):
    __tablename__ = 'registros_ventas'

    id = db.Column(db.Integer, primary_key=True)
    recibo = db.Column(db.String(100), unique=True)
    medio_pago_id = db.Column(db.Integer)
    entidad_banco_id = db.Column(db.Integer)
    area_id = db.Column(db.Integer)
    centro_costo_id = db.Column(db.Integer)
    detalle = db.Column(db.Text)
    empresa_id = db.Column(db.Integer)
    monto = db.Column(db.Numeric(10, 2))
    confirmado = db.Column(db.Boolean, default=False)
    fecha_registro_pago = db.Column(db.Date)
    fecha_comprobante = db.Column(db.Date)
    fecha_ingreso_cuenta = db.Column(db.Date)
    fecha_confirmacion_redes = db.Column(db.DateTime)
    fecha_confirmacion_gerencia = db.Column(db.DateTime)
    confirmado_redes = db.Column(db.Boolean, default=False)
    vendedor_id = db.Column(db.String(100))
    confirmado_por_gerencia = db.Column(db.String(100))
    confirmado_por_redes = db.Column(db.String(100))

    def estado_confirmacion(self):
        return "Confirmado" if self.confirmado else "Pendiente"

    def estado_redes(self):
        return "Confirmado" if self.confirmado_redes else "Pendiente"
