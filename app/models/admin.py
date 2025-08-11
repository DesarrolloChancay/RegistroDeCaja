# Archivo: app/models/admin.py

from app.extensions import db

class Admin(db.Model):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.String(100), db.ForeignKey('usuarios.id'), unique=True, nullable=False)
    # Puedes agregar más campos específicos del admin aquí

    def __repr__(self):
        return f'<Admin usuario_id={self.usuario_id}>'
