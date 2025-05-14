from flask import Blueprint, redirect, render_template, request, jsonify, url_for, flash
from MySQLdb.cursors import DictCursor
from app.db import conectar
from flask_login import current_user

product_bp = Blueprint("product", __name__)


@product_bp.route("/productos/<categoria_nombre>")
def productos_categoria(categoria_nombre):
    db = conectar()
    cursor = db.cursor(DictCursor)

    cursor.execute("SELECT id FROM categorias WHERE nombre = %s", (categoria_nombre,))
    categoria = cursor.fetchone()

    if not categoria:
        return "<h1>Categoría no encontrada</h1>", 404

    cursor.execute("""
        SELECT p.id, p.nombre_producto AS nombre, p.descripcion, p.precio, p.imagenes AS imagen,
            COALESCE((SELECT AVG(valor) FROM valoraciones WHERE producto_id = p.id), 0) AS media_valoracion
        FROM productos p 
        WHERE categoria_id = %s
    """, (categoria["id"],))
    productos = cursor.fetchall()

    
    cursor.close()
    db.close()

    return render_template("producto.html", categoria=categoria_nombre, productos=productos)

@product_bp.route("/producto/detalle/<int:producto_id>")
def producto(producto_id):  
    db = conectar()
    cursor = db.cursor(DictCursor)

    cursor.execute("""
        SELECT id, nombre_producto AS nombre, descripcion, precio, imagenes AS imagen 
        FROM productos WHERE id = %s
    """, (producto_id,))
    producto = cursor.fetchone()

    if not producto:
        return "<h1>Producto no encontrado</h1>", 404

    cursor.execute("""
        SELECT AVG(valor) AS media_valoracion FROM valoraciones WHERE producto_id = %s
    """, (producto_id,))
    resultado = cursor.fetchone()
    media_valoracion = round(resultado["media_valoracion"], 1) if resultado["media_valoracion"] else 0

    cursor.execute("""
        SELECT v.valor, v.comentario, v.fecha, u.nombre_completo AS usuario
        FROM valoraciones v
        JOIN usuarios u ON v.usuario_id = u.id
        WHERE v.producto_id = %s 
        ORDER BY v.fecha DESC
    """, (producto_id,))
    valoraciones = cursor.fetchall()



    cursor.close()
    db.close()

    return render_template("producto.html", producto=producto, media_valoracion=media_valoracion, valoraciones=valoraciones)

@product_bp.route("/buscar", methods=["GET"])
def buscar():
    query = request.args.get("q").strip()
    if len(query) < 4:
        return render_template("buscar.html", resultados=[], query=query)

    db = conectar()
    cursor = db.cursor(DictCursor)

    cursor.execute("""
        SELECT id, nombre_producto AS nombre, descripcion, precio, imagenes AS imagen 
        FROM productos 
        WHERE nombre_producto LIKE %s OR descripcion LIKE %s
        ORDER BY CHAR_LENGTH(nombre_producto) ASC  -- ✅ Prioriza nombres más cortos y exactos
    """, (f"%{query}%", f"%{query}%"))
    
    resultados = cursor.fetchall()
    
    cursor.close()
    db.close()

    return render_template("buscar.html", resultados=resultados, query=query)

@product_bp.route("/valorar/<int:producto_id>", methods=["POST"])
def valorar(producto_id):
    if not current_user.is_authenticated:
        return jsonify({"error": "Debes iniciar sesión para valorar un producto"}), 403

    valor = request.form.get("valor")
    comentario = request.form.get("comentario")

    if not valor:
        return jsonify({"error": "Selecciona una puntuación antes de enviar"}), 400

    db = conectar()
    cursor = db.cursor()

    cursor.execute("""
        INSERT INTO valoraciones (producto_id, usuario_id, valor, comentario) 
        VALUES (%s, %s, %s, %s)
    """, (producto_id, current_user.id, float(valor), comentario))

    db.commit()
    cursor.close()
    db.close()

    return jsonify({"mensaje": "¡Gracias por tu valoración!", "valoracion": float(valor)})


