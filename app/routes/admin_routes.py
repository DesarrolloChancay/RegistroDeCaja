
# Archivo: app/routes/admin_routes.py


from flask import Blueprint
from app.controllers import admin_controller

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin/editar_fecha_voucher', methods=['POST'])
def editar_fecha_voucher():
    return admin_controller.editar_fecha_voucher()

@admin_bp.route('/admin/editar_fecha_ingreso', methods=['POST'])
def editar_fecha_ingreso():
    return admin_controller.editar_fecha_ingreso()

@admin_bp.route('/mantenimiento')
def mantenimiento():
    return admin_controller.admin_mantenimiento()

@admin_bp.route('/admin/empresas/tabla')
def tabla_empresas():
    return admin_controller.tabla_empresas()

@admin_bp.route('/admin/empresas/agregar', methods=['POST'])
def agregar_empresa():
    return admin_controller.agregar_empresa()

@admin_bp.route('/admin/centros_costo/tabla')
def tabla_centros_costo():
    return admin_controller.tabla_centros_costo()

@admin_bp.route('/admin/centros_costo/agregar', methods=['POST'])
def agregar_centro_costo():
    return admin_controller.agregar_centro_costo()

@admin_bp.route('/admin/usuarios/tabla')
def tabla_usuarios():
    return admin_controller.tabla_usuarios()

@admin_bp.route('/admin/usuarios/agregar', methods=['POST'])
def agregar_usuario():
    return admin_controller.agregar_usuario()

@admin_bp.route('/admin/entidades_banco/tabla')
def tabla_entidades_banco():
    return admin_controller.tabla_entidades_banco()

@admin_bp.route('/admin/entidades_banco/agregar', methods=['POST'])
def agregar_entidad_banco():
    return admin_controller.agregar_entidad_banco()

@admin_bp.route('/admin/medios_pago/tabla')
def tabla_medios_pago():
    return admin_controller.tabla_medios_pago()

@admin_bp.route('/admin/medios_pago/agregar', methods=['POST'])
def agregar_medio_pago():
    return admin_controller.agregar_medio_pago()
