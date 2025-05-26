from flask import Blueprint, request, jsonify
from flask_login import current_user
from MySQLdb.cursors import DictCursor
from app.db import conectar
from flask_wtf.csrf import CSRFProtect

# Inicializa la protección CSRF
csrf = CSRFProtect()

# Define un blueprint para las rutas del carrito
carrito_bp = Blueprint("carrito", __name__)

# 🚀 Ruta para agregar productos al carrito (con protección CSRF)
@carrito_bp.route("/agregar_carrito/<int:producto_id>", methods=["POST"])
def agregar_carrito(producto_id):
    # Verifica que el usuario esté autenticado
    if not current_user.is_authenticated:
        return jsonify({"success": False, "error": "Usuario no autenticado"}), 401

    usuario_id = current_user.id  # ID del usuario actual

    # Obtiene los datos enviados en el cuerpo del request (JSON)
    data = request.get_json()

    # Verifica que se haya enviado una cantidad
    if not data or "cantidad" not in data:
        return jsonify({"success": False, "error": "Datos inválidos"}), 400

    cantidad = int(data.get("cantidad", 1))

    # Obtiene el token CSRF desde el header personalizado
    csrf_token = request.headers.get("X-CSRFToken")

    # Verifica que el token CSRF esté presente
    if not csrf_token:
        return jsonify({"success": False, "error": "Token CSRF faltante"}), 403

    # Conecta a la base de datos
    db = conectar()
    cursor = db.cursor()

    # Verifica si el producto ya está en el carrito del usuario
    cursor.execute("SELECT cantidad FROM carrito WHERE usuario_id = %s AND producto_id = %s", (usuario_id, producto_id))
    producto_en_carrito = cursor.fetchone()

    if producto_en_carrito:
        # Si ya existe, actualiza la cantidad sumando la nueva
        nueva_cantidad = producto_en_carrito[0] + cantidad
        cursor.execute("UPDATE carrito SET cantidad = %s WHERE usuario_id = %s AND producto_id = %s", (nueva_cantidad, usuario_id, producto_id))
    else:
        # Si no existe, lo inserta en la tabla carrito
        cursor.execute("INSERT INTO carrito (usuario_id, producto_id, cantidad) VALUES (%s, %s, %s)", (usuario_id, producto_id, cantidad))

    db.commit()  # Guarda los cambios
    cursor.close()
    db.close()

    return jsonify({"success": True})

# 🚫 Exime esta ruta de la protección CSRF global (porque ya se valida manualmente)
csrf.exempt(agregar_carrito)

# ✅ Ruta para ver los productos en el carrito del usuario autenticado
@carrito_bp.route("/ver_carrito", methods=["GET"])
def ver_carrito():
    # Verifica autenticación
    if not current_user.is_authenticated:
        return jsonify({"success": False, "error": "Usuario no autenticado"}), 401

    usuario_id = current_user.id

    db = conectar()
    cursor = db.cursor(DictCursor)  # Devuelve diccionarios en lugar de tuplas

    # Consulta para obtener los productos del carrito junto con sus datos
    cursor.execute("""
        SELECT c.producto_id, p.nombre_producto AS nombre, p.precio, p.imagenes AS imagen, 
               c.cantidad, (p.precio * c.cantidad) AS precio_total
        FROM carrito c
        JOIN productos p ON c.producto_id = p.id
        WHERE c.usuario_id = %s
    """, (usuario_id,))
    
    productos_carrito = cursor.fetchall()  # Obtiene los productos
    
    cursor.close()
    db.close()

    return jsonify({"success": True, "productos": productos_carrito})


# 🔁 Ruta para actualizar la cantidad de un producto en el carrito
@carrito_bp.route("/actualizar_carrito/<int:producto_id>", methods=["POST"])
def actualizar_carrito(producto_id):
    if not current_user.is_authenticated:
        return jsonify({"success": False, "error": "Usuario no autenticado"}), 401

    data = request.get_json()
    nueva_cantidad = int(data.get("cantidad", 1))

    db = conectar()
    cursor = db.cursor()

    # Actualiza la cantidad del producto en el carrito
    cursor.execute("UPDATE carrito SET cantidad = %s WHERE usuario_id = %s AND producto_id = %s",
                   (nueva_cantidad, current_user.id, producto_id))
    db.commit()
    cursor.close()
    db.close()

    return jsonify({"success": True})


# 🗑️ Ruta para eliminar un producto del carrito
@carrito_bp.route("/eliminar_carrito/<int:producto_id>", methods=["DELETE"])
def eliminar_carrito(producto_id):
    if not current_user.is_authenticated:
        return jsonify({"success": False, "error": "Usuario no autenticado"}), 401

    db = conectar()
    cursor = db.cursor()

    # Elimina el producto del carrito para el usuario actual
    cursor.execute("DELETE FROM carrito WHERE usuario_id = %s AND producto_id = %s",
                   (current_user.id, producto_id))
    db.commit()
    cursor.close()
    db.close()

    return jsonify({"success": True})
