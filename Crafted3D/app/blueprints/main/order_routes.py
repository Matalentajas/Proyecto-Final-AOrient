from flask import Blueprint, current_app, render_template, flash, redirect, session, url_for, request
from flask_login import current_user, login_required
from app.email_sender import enviar_correo_confirmacion_pedido
from app.db import conectar
from MySQLdb.cursors import DictCursor


order_bp = Blueprint("order", __name__)

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

    # Obtener el número de pedido más reciente
    cursor.execute("SELECT numero_pedido FROM pedidos ORDER BY id DESC LIMIT 1")
    ultimo_pedido = cursor.fetchone()

    if ultimo_pedido and ultimo_pedido["numero_pedido"]:
        try:
            ultimo_numero = int(ultimo_pedido["numero_pedido"][2:])
            nuevo_numero_pedido = f"ES{ultimo_numero + 1:06d}"
        except ValueError:
            nuevo_numero_pedido = "ES000001"
    else:
        nuevo_numero_pedido = "ES000001"

    # Obtener la dirección del usuario ANTES de usarla
    cursor.execute("""
        SELECT direccion_completa, ciudad, codigo_postal
        FROM usuarios
        WHERE id = %s
    """, (usuario_id,))
    usuario_info = cursor.fetchone()

    if not usuario_info:
        flash("No se pudo obtener la dirección del usuario.", "danger")
        cursor.close()
        db.close()
        return redirect(url_for("order.confirmar_pedido_vista"))

    # Obtener los productos del carrito
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
        cursor.close()
        db.close()
        return redirect(url_for("order.confirmar_pedido_vista"))

    # Calcular el total del pedido
    total_pedido = sum(producto["precio_total"] for producto in carrito)

    # Insertar el pedido con el número generado y la dirección
    cursor.execute("""
        INSERT INTO pedidos (usuario_id, numero_pedido, estado_pago, estado, total, direccion, ciudad, codigo_postal)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        usuario_id, nuevo_numero_pedido, "Pendiente", "Procesando", total_pedido,
        usuario_info["direccion_completa"], usuario_info["ciudad"], usuario_info["codigo_postal"]
    ))
    
    pedido_id = cursor.lastrowid  # Obtener el ID del pedido recién creado

    # Registrar los productos dentro del pedido
    for producto in carrito:
        cursor.execute("""INSERT INTO pedido_detalles 
                          (pedido_id, producto_id, cantidad, precio) 
                          VALUES (%s, %s, %s, %s)""",
                       (pedido_id, producto["producto_id"], producto["cantidad"], producto["precio_total"]))

    # Vaciar el carrito del usuario
    cursor.execute("DELETE FROM carrito WHERE usuario_id = %s", (usuario_id,))

    # Preparar datos para el correo
    pedido = {
        "productos": carrito,
        "total": total_pedido
    }

    enviar_correo_confirmacion_pedido(
        current_user.email, current_user.nombre_completo, nuevo_numero_pedido, pedido,
        usuario_info["direccion_completa"], usuario_info["ciudad"], usuario_info["codigo_postal"]
    )

    db.commit()
    cursor.close()
    db.close()

    # Redirigir al usuario a la página del pedido confirmado
    return render_template("pedido_confirmado.html", usuario=current_user, numero_pedido=nuevo_numero_pedido)


@order_bp.route("/pedido_info/<numero>")
@login_required
def pedido_info(numero):
    print("DEBUG - Cargando pedido_info con número:", numero)
    cursor = current_app.mysql.connection.cursor()

    cursor.execute("""
        SELECT id, numero_pedido, fecha_pedido, estado_pago, estado, total,
            direccion, ciudad, codigo_postal
        FROM pedidos WHERE numero_pedido = %s
    """, (numero,))
    pedido_data = cursor.fetchone()

    if not pedido_data:
        flash("El pedido no existe o no tienes acceso a él.", "danger")
        return redirect(url_for("usuario.perfil"))

    pedido_id = pedido_data[0]

    cursor.execute("""
        SELECT p.nombre_producto, p.imagenes, d.cantidad, d.precio 
        FROM pedido_detalles d
        JOIN productos p ON d.producto_id = p.id
        WHERE d.pedido_id = %s
    """, (pedido_id,))
    
    productos_raw = cursor.fetchall()
    cursor.close()

    productos = [
        {
            "nombre": row[0],
            "imagen": row[1].split(',')[0],  # Tomar primera imagen
            "cantidad": row[2],
            "precio": float(row[3])
        }
        for row in productos_raw
    ]

    total = float(pedido_data[5])
    iva = round(total * 0.21, 2)
    envio = 5.00  # si tienes envío fijo
    subtotal = round(total - iva - envio, 2)

    pedido_info = {
        "numero": pedido_data[1],
        "fecha": pedido_data[2].strftime("%Y-%m-%d %H:%M:%S"),
        "estado_pago": pedido_data[3],
        "estado": pedido_data[4],
        "total": total,
        "iva": iva,
        "envio": envio,
        "subtotal": subtotal,
        "productos": productos,
        "direccion": {
            "calle": pedido_data[6],
            "ciudad": pedido_data[7],
            "codigo_postal": pedido_data[8]
        }   
    }

    return render_template("pedido.html", pedido=pedido_info)






