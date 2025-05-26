from flask import Blueprint, current_app, render_template, flash, redirect, session, url_for, request
from flask_login import current_user, login_required
from app.email_sender import enviar_correo_confirmacion_pedido
from app.db import conectar
from MySQLdb.cursors import DictCursor
from datetime import timedelta

order_bp = Blueprint("order", __name__)

@order_bp.route("/confirmar_pedido", methods=["GET"])
@login_required
def confirmar_pedido_vista():
    # Obtener el ID del usuario actualmente logueado
    usuario_id = current_user.id  

    # Conectar a la base de datos y obtener cursor que devuelve diccionarios
    db = conectar()
    cursor = db.cursor(DictCursor)

    # Consultar datos del usuario (nombre, email, dirección, ciudad, código postal)
    cursor.execute("""
        SELECT nombre_completo, email, direccion_completa, codigo_postal, ciudad
        FROM usuarios
        WHERE id = %s
    """, (usuario_id,))
    
    usuario = cursor.fetchone()  # Obtener los datos del usuario

    # Consultar los productos que tiene el usuario en su carrito
    cursor.execute("""
        SELECT c.producto_id, p.nombre_producto AS nombre, p.precio, c.cantidad, 
            (p.precio * c.cantidad) AS precio_total, p.imagenes AS imagen
        FROM carrito c
        JOIN productos p ON c.producto_id = p.id
        WHERE c.usuario_id = %s
    """, (usuario_id,))

    productos_carrito = cursor.fetchall()  # Lista de productos con sus datos y cantidad

    # Cerrar cursor y conexión
    cursor.close()
    db.close()

    # Crear un diccionario con los productos y el total calculado del pedido
    pedido = {"productos": productos_carrito, "total": sum(p["precio_total"] for p in productos_carrito)}

    # Renderizar la plantilla para confirmar pedido, pasando datos del usuario y del pedido
    return render_template("confirmar_pedido.html", usuario=usuario, pedido=pedido)


@order_bp.route("/procesar_pedido", methods=["POST"])
@login_required
def procesar_pedido():
    usuario_id = current_user.id  

    db = conectar()
    cursor = db.cursor(DictCursor)

    # Obtener el número de pedido más reciente para generar uno nuevo único y secuencial
    cursor.execute("SELECT numero_pedido FROM pedidos ORDER BY id DESC LIMIT 1")
    ultimo_pedido = cursor.fetchone()

    # Generar nuevo número de pedido, formateado con prefijo 'ES' y 6 dígitos numéricos
    if ultimo_pedido and ultimo_pedido["numero_pedido"]:
        try:
            ultimo_numero = int(ultimo_pedido["numero_pedido"][2:])
            nuevo_numero_pedido = f"ES{ultimo_numero + 1:06d}"
        except ValueError:
            # Si el formato no es correcto, iniciar en ES000001
            nuevo_numero_pedido = "ES000001"
    else:
        nuevo_numero_pedido = "ES000001"

    # Obtener la dirección del usuario para guardar en el pedido
    cursor.execute("""
        SELECT direccion_completa, ciudad, codigo_postal
        FROM usuarios
        WHERE id = %s
    """, (usuario_id,))
    usuario_info = cursor.fetchone()

    # Si no se pudo obtener la dirección, informar al usuario y redirigir
    if not usuario_info:
        flash("No se pudo obtener la dirección del usuario.", "danger")
        cursor.close()
        db.close()
        return redirect(url_for("order.confirmar_pedido_vista"))

    # Obtener los productos actuales en el carrito para crear el detalle del pedido
    cursor.execute("""
        SELECT c.producto_id, p.nombre_producto AS nombre, p.precio, c.cantidad, 
               (p.precio * c.cantidad) AS precio_total
        FROM carrito c
        JOIN productos p ON c.producto_id = p.id
        WHERE c.usuario_id = %s
    """, (usuario_id,))
    
    carrito = cursor.fetchall()

    # Si el carrito está vacío, informar y redirigir
    if not carrito:
        flash("El carrito está vacío.", "danger")
        cursor.close()
        db.close()
        return redirect(url_for("order.confirmar_pedido_vista"))

    # Calcular el total del pedido sumando el precio_total de cada producto
    total_pedido = sum(producto["precio_total"] for producto in carrito)

    # Insertar el nuevo pedido en la tabla pedidos con todos los datos necesarios
    cursor.execute("""
        INSERT INTO pedidos (usuario_id, numero_pedido, estado_pago, estado, total, direccion, ciudad, codigo_postal)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        usuario_id, nuevo_numero_pedido, "Pendiente", "Procesando", total_pedido,
        usuario_info["direccion_completa"], usuario_info["ciudad"], usuario_info["codigo_postal"]
    ))
    
    pedido_id = cursor.lastrowid  # Obtener el ID del pedido recién insertado

    # Insertar cada producto del carrito en la tabla de detalles del pedido
    for producto in carrito:
        cursor.execute("""INSERT INTO pedido_detalles 
                          (pedido_id, producto_id, cantidad, precio) 
                          VALUES (%s, %s, %s, %s)""",
                       (pedido_id, producto["producto_id"], producto["cantidad"], producto["precio_total"]))

    # Vaciar el carrito del usuario para dejarlo limpio después del pedido
    cursor.execute("DELETE FROM carrito WHERE usuario_id = %s", (usuario_id,))

    # Preparar datos del pedido para enviar en el correo de confirmación
    pedido = {
        "productos": carrito,
        "total": total_pedido
    }

    # Enviar correo de confirmación al usuario con los datos del pedido
    enviar_correo_confirmacion_pedido(
        current_user.email, current_user.nombre_completo, nuevo_numero_pedido, pedido,
        usuario_info["direccion_completa"], usuario_info["ciudad"], usuario_info["codigo_postal"]
    )

    # Confirmar todos los cambios en la base de datos
    db.commit()
    cursor.close()
    db.close()

    # Renderizar la página de pedido confirmado con información para el usuario
    return render_template("pedido_confirmado.html", usuario=current_user, numero_pedido=nuevo_numero_pedido)


@order_bp.route("/pedido_info/<numero>")
@login_required
def pedido_info(numero):
    print("DEBUG - Cargando pedido_info con número:", numero)

    # Conectar a la base de datos
    db = conectar()
    cursor = db.cursor()

    # Consultar los datos generales del pedido por su número único
    cursor.execute("""
        SELECT id, numero_pedido, fecha_pedido, estado_pago, estado, total,
            direccion, ciudad, codigo_postal
        FROM pedidos WHERE numero_pedido = %s
    """, (numero,))
    pedido_data = cursor.fetchone()

    # Si no existe el pedido o no pertenece al usuario, mostrar error y redirigir
    if not pedido_data:
        flash("El pedido no existe o no tienes acceso a él.", "danger")
        cursor.close()
        db.close()
        return redirect(url_for("usuario.perfil"))

    pedido_id = pedido_data[0]  # Obtener ID interno del pedido

    # Consultar los productos asociados a ese pedido
    cursor.execute("""
        SELECT p.nombre_producto, p.imagenes, d.cantidad, d.precio 
        FROM pedido_detalles d
        JOIN productos p ON d.producto_id = p.id
        WHERE d.pedido_id = %s
    """, (pedido_id,))
    
    productos_raw = cursor.fetchall()
    cursor.close()
    db.close()

    # Procesar la lista de productos para estructurarla en diccionarios legibles
    productos = [
        {
            "nombre": row[0],
            "imagen": row[1].split(',')[0],  # Usar la primera imagen (si hay varias)
            "cantidad": row[2],
            "precio": float(row[3])
        }
        for row in productos_raw
    ]

    total = float(pedido_data[5])  # Precio total del pedido
    iva = round(total * 0.21, 2)  # Calcular IVA al 21%
    envio = 5.00  # Coste fijo de envío
    subtotal = round(total - iva - envio, 2)  # Subtotal sin IVA y envío

    # Construir diccionario con toda la información para la plantilla
    # Ajustar la hora a la zona horaria de España (UTC+2 en horario de verano, UTC+1 en invierno)
    # Aquí sumamos 2 horas como ejemplo (ajusta según corresponda)
    fecha_pedido = pedido_data[2] + timedelta(hours=2)
    pedido_info = {
        "numero": pedido_data[1],
        "fecha": fecha_pedido.strftime("%Y-%m-%d %H:%M:%S"),
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

    # Renderizar plantilla con la información completa del pedido
    return render_template("pedido.html", pedido=pedido_info)
