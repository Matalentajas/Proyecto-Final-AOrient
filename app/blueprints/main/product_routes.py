from flask import Blueprint, render_template, request, jsonify
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

    cursor.execute("SELECT id, nombre_producto AS nombre, descripcion, precio, imagenes AS imagen FROM productos WHERE id = %s", (producto_id,))
    producto = cursor.fetchone()
    
    cursor.close()
    db.close()

    if not producto:
        return "<h1>Producto no encontrado</h1>", 404

    return render_template("producto.html", producto=producto)

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