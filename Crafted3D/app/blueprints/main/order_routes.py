from flask import Blueprint, render_template, flash, redirect, session, url_for, request
from flask_login import current_user, login_required
from app.db import conectar
from MySQLdb.cursors import DictCursor


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



@order_bp.route("/confirmar_pedido", methods=["GET"])
@login_required
def confirmar_pedido():
    usuario_id = current_user.id  

    db = conectar()
    cursor = db.cursor(DictCursor)

    # 🚀 Obtener datos del usuario
    cursor.execute("""
        SELECT nombre_completo, email, direccion_completa, codigo_postal, ciudad
        FROM usuarios
        WHERE id = %s
    """, (usuario_id,))
    
    usuario = cursor.fetchone()  # Extraer los datos del usuario

    # 🚀 Obtener los productos del carrito
    cursor.execute("""
        SELECT c.producto_id, p.nombre_producto AS nombre, p.precio, c.cantidad, 
            (p.precio * c.cantidad) AS precio_total, p.imagenes AS imagen
        FROM carrito c
        JOIN productos p ON c.producto_id = p.id
        WHERE c.usuario_id = %s
    """, (usuario_id,))

    
    productos_carrito = cursor.fetchall()

    cursor.close()
    db.close()

    pedido = {"productos": productos_carrito, "total": sum(p["precio_total"] for p in productos_carrito)}

    return render_template("confirmar_pedido.html", usuario=usuario, pedido=pedido)





