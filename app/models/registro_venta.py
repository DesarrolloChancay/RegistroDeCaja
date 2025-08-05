from app import db
from datetime import datetime

class RegistroVenta(db.Model):
    __tablename__ = 'registros_ventas'

    id = db.Column(db.Integer, primary_key=True)
    fecha_comprobante = db.Column(db.Date)
    recibo = db.Column(db.String(100), unique=True)
    detalle = db.Column(db.Text)
    monto = db.Column(db.Numeric(10, 2))
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)

    entidad_banco_id = db.Column(db.Integer, db.ForeignKey('entidades_banco.id'))
    medio_pago_id = db.Column(db.Integer, db.ForeignKey('medios_pago.id'))
    empresa_id = db.Column(db.Integer, db.ForeignKey('empresas.id'))
    confirmado = db.Column(db.Boolean, default=False)
    fecha_pago_recibido = db.Column(db.Date)
    confirmado_redes = db.Column(db.Boolean, default=False)
    fecha_confirmacion_redes = db.Column(db.Date)
    fecha_confirmacion = db.Column(db.Date)

    # relaciones si las necesitas (empresa, banco, etc.)

    def estado_confirmacion(self):
        return "Confirmado" if self.confirmado else "Pendiente"

    def estado_redes(self):
        return "Confirmado" if self.confirmado_redes else "Pendiente"
