from flask import Blueprint, render_template
from MySQLdb.cursors import DictCursor
from app.db import conectar

product_bp = Blueprint("product", __name__)

@product_bp.route("/productos/<categoria_nombre>")
def productos_categoria(categoria_nombre):
    db = conectar()
    cursor = db.cursor(DictCursor)

    # Obtener el ID de la categoría usando su nombre
    cursor.execute("SELECT id FROM categorias WHERE nombre = %s", (categoria_nombre,))
    categoria = cursor.fetchone()

    if not categoria:
        return "<h1>Categoría no encontrada</h1>", 404

    # Obtener los productos de esa categoría
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

