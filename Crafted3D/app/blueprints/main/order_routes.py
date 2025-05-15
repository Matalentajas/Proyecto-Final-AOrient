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
def confirmar_pedido_vista():
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

@order_bp.route("/procesar_pedido", methods=["POST"])
@login_required
def procesar_pedido():
    usuario_id = current_user.id  

    db = conectar()
    cursor = db.cursor(DictCursor)

    # 🚀 Obtener el número de pedido más reciente
    cursor.execute("SELECT numero_pedido FROM pedidos ORDER BY id DESC LIMIT 1")
    ultimo_pedido = cursor.fetchone()

    if ultimo_pedido:
        # Extraer el número y aumentarlo en 1
        ultimo_numero = int(ultimo_pedido["numero_pedido"][2:])  # Eliminar "ES" y convertir a número
        nuevo_numero_pedido = f"ES{ultimo_numero + 1:06d}"  # Formato con ceros a la izquierda
    else:
        nuevo_numero_pedido = "ES000001"  # Primer pedido

    # 🚀 Obtener los productos del carrito
    cursor.execute("""
        SELECT c.producto_id, p.nombre_producto AS nombre, p.precio, c.cantidad, 
               (p.precio * c.cantidad) AS precio_total
        FROM carrito c
        JOIN productos p ON c.producto_id = p.id
        WHERE c.usuario_id = %s
    """, (usuario_id,))
    
    carrito = cursor.fetchall()

    if not carrito:
        flash("El carrito está vacío.", "danger")
        return redirect(url_for("order.confirmar_pedido"))  # Vuelve a la página si el carrito está vacío

    # 🚀 Calcular el total del pedido
    total_pedido = sum(producto["precio_total"] for producto in carrito)

    # 🚀 Insertar el pedido con el número generado
    cursor.execute("INSERT INTO pedidos (usuario_id, numero_pedido, estado_pago, estado, total) VALUES (%s, %s, %s, %s, %s)", 
                   (usuario_id, nuevo_numero_pedido, "Pendiente", "Procesando", total_pedido))
    
    pedido_id = cursor.lastrowid  # Obtener el ID del pedido recién creado

    # 🚀 Registrar los productos dentro del pedido
    for producto in carrito:
        cursor.execute("""INSERT INTO pedido_detalles 
                          (pedido_id, producto_id, cantidad, precio) 
                          VALUES (%s, %s, %s, %s)""",
                       (pedido_id, producto["producto_id"], producto["cantidad"], producto["precio_total"]))

    # 🚮 Vaciar el carrito del usuario
    cursor.execute("DELETE FROM carrito WHERE usuario_id = %s", (usuario_id,))

    db.commit()
    cursor.close()
    db.close()

    flash(f"¡Pedido confirmado! Número: {nuevo_numero_pedido}", "success")

    # 🚀 Redirigir al usuario a la página del pedido confirmado
    return redirect(url_for("order.pedido", numero=pedido_id))





