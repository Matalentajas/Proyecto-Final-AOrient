from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required

order_bp = Blueprint("order", __name__)

usuario = {
    "nombre": "Juan Pérez",
    "direccion": "Calle Falsa 123",
    "codigo_postal": "28080",
    "ciudad": "Madrid",
    "pais": "España"
}

# Lista de pedidos de ejemplo
pedidos = [
    {
        "numero": "PED12345",
        "fecha": "2025-05-01",
        "estado_pago": "Pagado",
        "estado": "Completado",
        "total": 150.00
    },
    {
        "numero": "PED12346",
        "fecha": "2025-05-03",
        "estado_pago": "Procesando",
        "estado": "Enviado",
        "total": 75.50
    },
    {
        "numero": "PED12347",
        "fecha": "2025-05-05",
        "estado_pago": "Pendiente",
        "estado": "Cancelado",
        "total": 200.00
    }
]

pedido_actual = {"numero": "ES999XYZ", "fecha": "12/05/2025", "estado_pago": "Pendiente", "total": "41,29"}

@order_bp.route("/pedido/<numero>")
@login_required
def pedido(numero):
    pedido = next((p for p in pedidos if p["numero"] == numero), None)
    if not pedido:
        flash("Pedido no encontrado.", "danger")
        return redirect(url_for("usuario.perfil"))
    return render_template("pedido.html", pedido=pedido)

@order_bp.route("/confirmar_pedido", methods=["GET", "POST"])
@login_required
def confirmar_pedido():
    if request.method == "POST":
        flash("Pedido confirmado!", "success")
        return redirect(url_for("order.pedido", numero=pedido_actual["numero"]))
    return render_template("confirmar_pedido.html", usuario=usuario, pedido=pedido_actual)
