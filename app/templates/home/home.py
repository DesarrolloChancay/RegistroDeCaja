# rutas/home.py

from flask import Blueprint, render_template, jsonify, request

home_bp = Blueprint('home', __name__)


@home_bp.route('/')
def home():
    return render_template('home.html')


# Datos de auditoría simulados
datos_auditoria = [
    {
        "fecha_registro": "2025-08-03 05:00:00",
        "transaccion": "TRANS-001",
        "empresa": "Resource",
        "banco": "Banco X",
        "monto": 150.00,
        "detalle": "Venta de entradas para evento X",
        "fecha_voucher_confirmacion": "",
        "confirmacion_redes": "Pendiente",
        "fecha_ingreso_dinero": "",
        "confirmar_pago": "Pendiente"
    },
    {
        "fecha_registro": "2025-08-03 05:02:00",
        "transaccion": "TRANS-002",
        "empresa": "Resource",
        "banco": "Banco Y",
        "monto": 480.00,
        "detalle": "Venta de entradas para evento X",
        "fecha_voucher_confirmacion": "",
        "confirmacion_redes": "Pendiente",
        "fecha_ingreso_dinero": "",
        "confirmar_pago": "Condirmado"
    },
    {
        "fecha_registro": "2025-08-03 05:04:00",
        "transaccion": "TRANS-003",
        "empresa": "Resource",
        "banco": "Banco Z",
        "monto": 290.00,
        "detalle": "Venta de entradas para evento X",
        "fecha_voucher_confirmacion": "",
        "confirmacion_redes": "Confirmado",
        "fecha_ingreso_dinero": "",
        "confirmar_pago": "Pendiente"
    }
]


@home_bp.route('/')
def index():
    return render_template('home.html')


@home_bp.route('/api/auditoria')
def get_auditoria():
    return jsonify(datos_auditoria)


@home_bp.route('/api/exportar', methods=['POST'])
def exportar():
    fecha = request.json.get('fecha')
    return jsonify({"mensaje": f"Exportación de datos para la fecha {fecha} generada correctamente."})
