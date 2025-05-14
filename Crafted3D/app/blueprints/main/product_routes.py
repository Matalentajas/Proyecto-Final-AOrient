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

    cursor.execute("SELECT id, nombre_producto AS nombre, descripcion, precio, imagenes AS imagen FROM productos WHERE categoria_id = %s", (categoria["id"],))
    productos = cursor.fetchall()
    
    cursor.close()
    db.close()

    return render_template("producto.html", categoria=categoria_nombre, productos=productos)

@product_bp.route("/producto/<int:producto_id>")
def producto(producto_id):
    db = conectar()
    cursor = db.cursor(DictCursor)

    cursor.execute("""
        SELECT id, nombre_producto AS nombre, descripcion, precio, imagenes AS imagen 
        FROM productos WHERE id = %s
    """, (producto_id,))
    producto = cursor.fetchone()

    cursor.execute("""
        SELECT valor, comentario, fecha 
        FROM valoraciones WHERE producto_id = %s 
        ORDER BY fecha DESC
    """, (producto_id,))
    valoraciones = cursor.fetchall()
    
    cursor.close()
    db.close()

    if not producto:
        return "<h1>Producto no encontrado</h1>", 404

    return render_template("producto.html", producto=producto, valoraciones=valoraciones)


@product_bp.route("/productos_destacados")
def productos_destacados():
    db = conectar()
    cursor = db.cursor(DictCursor)

    cursor.execute("""
        SELECT id, nombre_producto AS nombre, descripcion, precio, imagenes AS imagen 
        FROM productos 
        WHERE categoria_id IN (
            SELECT id FROM categorias WHERE nombre IN ('Escayolas3D', 'Decoracion', 'Juguetes')
        )
        LIMIT 3
    """)
    productos = cursor.fetchall()
    
    cursor.close()
    db.close()

    return render_template("index.html", productos_destacados=productos)

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


