from app.extensions import db
from datetime import datetime


class RegistroVenta(db.Model):
    __tablename__ = 'registros_ventas'

    id = db.Column(db.Integer, primary_key=True)
    fecha_comprobante = db.Column(db.Date)
    recibo = db.Column(db.String(100), unique=True)

    medio_pago_id = db.Column(db.Integer, db.ForeignKey('medios_pago.id'))
    entidad_banco_id = db.Column(
        db.Integer, db.ForeignKey('entidades_banco.id'))
    area_id = db.Column(db.Integer, db.ForeignKey('areas.id'))
    centro_costo_id = db.Column(db.Integer, db.ForeignKey('centros_costo.id'))
    empresa_id = db.Column(db.Integer, db.ForeignKey('empresas.id'))

    detalle = db.Column(db.Text)
    monto = db.Column(db.Numeric(10, 2))

    confirmado = db.Column(db.Boolean, default=False)
    fecha_pago_recibido = db.Column(db.Date)

    confirmado_redes = db.Column(db.Boolean, default=False)
    fecha_confirmacion_redes = db.Column(db.Date)

    vendedor_id = db.Column(db.String(100), db.ForeignKey('usuarios.id'))
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)

    confirmado_por_gerencia = db.Column(
        db.String(100), db.ForeignKey('usuarios.id'))
    confirmado_por_redes = db.Column(
        db.String(100), db.ForeignKey('usuarios.id'))

    fecha_confirmacion = db.Column(db.Date)

    # Relaciones (si quieres acceder a los objetos relacionados)
    medio_pago = db.relationship('MedioPago', backref='ventas')
    entidad_banco = db.relationship('EntidadBancaria', backref='ventas')
    area = db.relationship('Area', backref='ventas')
    centro_costo = db.relationship('CentroCosto', backref='ventas')
    empresa = db.relationship('Empresa', backref='ventas')

    vendedor = db.relationship('Usuario', foreign_keys=[vendedor_id])
    gerente_confirmador = db.relationship(
        'Usuario', foreign_keys=[confirmado_por_gerencia])
    red_confirmador = db.relationship(
        'Usuario', foreign_keys=[confirmado_por_redes])

    # relaciones si las necesitas (empresa, banco, etc.)

    def estado_confirmacion(self):
        return "Confirmado" if self.confirmado else "Pendiente"

    def estado_redes(self):
        return "Confirmado" if self.confirmado_redes else "Pendiente"
