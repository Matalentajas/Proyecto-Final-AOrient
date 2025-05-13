from flask import Blueprint, request, jsonify
from flask_login import current_user
from MySQLdb.cursors import DictCursor
from app.db import conectar
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect()
carrito_bp = Blueprint("carrito", __name__)

# 🚀 **Añadir al carrito con CSRF activado**
@carrito_bp.route("/agregar_carrito/<int:producto_id>", methods=["POST"])
def agregar_carrito(producto_id):
    if not current_user.is_authenticated:
        return jsonify({"success": False, "error": "Usuario no autenticado"}), 401

    usuario_id = current_user.id  
    data = request.get_json()

    if not data or "cantidad" not in data:
        return jsonify({"success": False, "error": "Datos inválidos"}), 400

    cantidad = int(data.get("cantidad", 1))
    csrf_token = request.headers.get("X-CSRFToken")

    # 🚀 **Validar el token CSRF**
    if not csrf_token:
        return jsonify({"success": False, "error": "Token CSRF faltante"}), 403

    db = conectar()
    cursor = db.cursor()

    cursor.execute("SELECT cantidad FROM carrito WHERE usuario_id = %s AND producto_id = %s", (usuario_id, producto_id))
    producto_en_carrito = cursor.fetchone()

    if producto_en_carrito:
        nueva_cantidad = producto_en_carrito[0] + cantidad
        cursor.execute("UPDATE carrito SET cantidad = %s WHERE usuario_id = %s AND producto_id = %s", (nueva_cantidad, usuario_id, producto_id))
    else:
        cursor.execute("INSERT INTO carrito (usuario_id, producto_id, cantidad) VALUES (%s, %s, %s)", (usuario_id, producto_id, cantidad))

    db.commit()
    cursor.close()
    db.close()

    return jsonify({"success": True})

csrf.exempt(agregar_carrito)

@carrito_bp.route("/ver_carrito", methods=["GET"])
def ver_carrito():
    if not current_user.is_authenticated:
        return jsonify({"success": False, "error": "Usuario no autenticado"}), 401

    usuario_id = current_user.id  

    db = conectar()
    cursor = db.cursor(DictCursor)

    cursor.execute("""
        SELECT c.producto_id, p.nombre_producto AS nombre, p.precio, p.imagenes AS imagen, 
               c.cantidad, (p.precio * c.cantidad) AS precio_total
        FROM carrito c
        JOIN productos p ON c.producto_id = p.id
        WHERE c.usuario_id = %s
    """, (usuario_id,))
    
    productos_carrito = cursor.fetchall()
    
    cursor.close()
    db.close()

    return jsonify({"success": True, "productos": productos_carrito})


@carrito_bp.route("/actualizar_carrito/<int:producto_id>", methods=["POST"])
def actualizar_carrito(producto_id):
    if not current_user.is_authenticated:
        return jsonify({"success": False, "error": "Usuario no autenticado"}), 401

    data = request.get_json()
    nueva_cantidad = int(data.get("cantidad", 1))

    db = conectar()
    cursor = db.cursor()
    cursor.execute("UPDATE carrito SET cantidad = %s WHERE usuario_id = %s AND producto_id = %s",
                   (nueva_cantidad, current_user.id, producto_id))
    db.commit()
    cursor.close()
    db.close()

    return jsonify({"success": True})


@carrito_bp.route("/eliminar_carrito/<int:producto_id>", methods=["DELETE"])
def eliminar_carrito(producto_id):
    if not current_user.is_authenticated:
        return jsonify({"success": False, "error": "Usuario no autenticado"}), 401

    db = conectar()
    cursor = db.cursor()
    cursor.execute("DELETE FROM carrito WHERE usuario_id = %s AND producto_id = %s",
                   (current_user.id, producto_id))
    db.commit()
    cursor.close()
    db.close()

    return jsonify({"success": True})

