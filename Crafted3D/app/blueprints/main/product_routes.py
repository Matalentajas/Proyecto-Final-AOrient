from flask import Blueprint, redirect, render_template, request, jsonify, url_for, flash
from MySQLdb.cursors import DictCursor
from app.db import conectar
from flask_login import current_user

# Crear un blueprint llamado "product" para agrupar rutas relacionadas con productos
product_bp = Blueprint("product", __name__)


# Ruta para mostrar productos de una categoría, con opción de filtrar orden de los resultados
@product_bp.route("/productos/<categoria_nombre>/", defaults={'filtro': 'mas-baratos'})
@product_bp.route("/productos/<categoria_nombre>/<filtro>")
def productos_categoria(categoria_nombre, filtro):
    # Conectar a la base de datos y usar cursor que devuelve resultados como diccionarios
    db = conectar()
    cursor = db.cursor(DictCursor)

    # Buscar el ID de la categoría a partir del nombre proporcionado en la URL
    cursor.execute("SELECT id FROM categorias WHERE nombre = %s", (categoria_nombre,))
    categoria = cursor.fetchone()

    # Si no se encuentra la categoría, devolver error 404 con mensaje
    if not categoria:
        return "<h1>Categoría no encontrada</h1>", 404

    # Definir la ordenación SQL según el filtro recibido (por defecto, más baratos)
    orden = "precio ASC"
    if filtro == "mas-caros":
        orden = "precio DESC"
    elif filtro == "mejor-valorados":
        orden = "media_valoracion DESC"

    # Consulta para obtener los productos de la categoría, calculando también la media de valoraciones
    cursor.execute(f"""
        SELECT p.id, p.nombre_producto AS nombre, p.descripcion, p.precio, p.imagenes AS imagen,
               COALESCE((SELECT AVG(valor) FROM valoraciones WHERE producto_id = p.id), 0) AS media_valoracion
        FROM productos p 
        WHERE categoria_id = %s
        ORDER BY {orden}
    """, (categoria["id"],))
    productos = cursor.fetchall()

    # Cerrar la conexión y el cursor
    cursor.close()
    db.close()

    # Renderizar la plantilla mostrando la categoría, productos y filtro activo
    return render_template("producto.html", categoria=categoria_nombre, productos=productos, filtro=filtro)


# Ruta para mostrar el detalle de un producto específico, incluyendo valoraciones
@product_bp.route("/producto/detalle/<int:producto_id>")
def producto(producto_id):  
    db = conectar()
    cursor = db.cursor(DictCursor)

    # Obtener datos básicos del producto según su ID
    cursor.execute("""
        SELECT id, nombre_producto AS nombre, descripcion, precio, imagenes AS imagen 
        FROM productos WHERE id = %s
    """, (producto_id,))
    producto = cursor.fetchone()

    # Si no existe el producto, devolver error 404 con mensaje
    if not producto:
        return "<h1>Producto no encontrado</h1>", 404

    # Calcular la media de valoraciones para ese producto
    cursor.execute("""
        SELECT AVG(valor) AS media_valoracion FROM valoraciones WHERE producto_id = %s
    """, (producto_id,))
    resultado = cursor.fetchone()
    media_valoracion = round(resultado["media_valoracion"], 1) if resultado["media_valoracion"] else 0

    # Obtener todas las valoraciones con comentarios, ordenadas de más reciente a más antiguo
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

    # Renderizar la plantilla de detalle con producto, media de valoraciones y lista de valoraciones
    return render_template("producto.html", producto=producto, media_valoracion=media_valoracion, valoraciones=valoraciones)


# Ruta para buscar productos que coincidan con una consulta de texto en nombre o descripción
@product_bp.route("/buscar", methods=["GET"])
def buscar():
    query = request.args.get("q").strip()  # Obtener el término de búsqueda desde el parámetro "q"
    
    # Si la consulta es demasiado corta, mostrar plantilla sin resultados para no saturar búsquedas
    if len(query) < 4:
        return render_template("buscar.html", resultados=[], query=query)

    db = conectar()
    cursor = db.cursor(DictCursor)

    # Buscar productos cuyo nombre o descripción contenga la consulta, priorizando nombres más cortos
    cursor.execute("""
        SELECT id, nombre_producto AS nombre, descripcion, precio, imagenes AS imagen 
        FROM productos 
        WHERE nombre_producto LIKE %s OR descripcion LIKE %s
        ORDER BY CHAR_LENGTH(nombre_producto) ASC
    """, (f"%{query}%", f"%{query}%"))
    
    resultados = cursor.fetchall()
    
    cursor.close()
    db.close()

    # Renderizar plantilla de búsqueda con resultados y consulta mostrada
    return render_template("buscar.html", resultados=resultados, query=query)


# Ruta para que un usuario logueado pueda valorar un producto con puntuación y comentario
@product_bp.route("/valorar/<int:producto_id>", methods=["POST"])
def valorar(producto_id):
    # Verificar que el usuario esté autenticado
    if not current_user.is_authenticated:
        return jsonify({"error": "Debes iniciar sesión para valorar un producto"}), 403

    valor = request.form.get("valor")  # Obtener la puntuación enviada por el usuario
    comentario = request.form.get("comentario")  # Obtener el comentario enviado

    # Validar que se haya enviado una puntuación
    if not valor:
        return jsonify({"error": "Selecciona una puntuación antes de enviar"}), 400

    db = conectar()
    cursor = db.cursor()

    # Insertar la valoración en la base de datos, vinculando producto y usuario
    cursor.execute("""
        INSERT INTO valoraciones (producto_id, usuario_id, valor, comentario) 
        VALUES (%s, %s, %s, %s)
    """, (producto_id, current_user.id, float(valor), comentario))

    db.commit()
    cursor.close()
    db.close()

    # Devolver mensaje JSON de éxito con la valoración enviada
    return jsonify({"mensaje": "¡Gracias por tu valoración!", "valoracion": float(valor)})
