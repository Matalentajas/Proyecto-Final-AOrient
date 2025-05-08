from flask import Blueprint, render_template

product_bp = Blueprint("product", __name__)

productos_por_categoria = {
    'escayolas3D': [
        {'id': 'escayola3D_01', 'nombre': 'Escayola 3D Modelo A', 'precio': '19,99 €', 'imagen': 'producto-generico.jpg', 'descripcion': 'Transforma cualquier espacio con su diseño único.'},
        {'id': 'escayola3D_02', 'nombre': 'Escayola 3D Modelo B', 'precio': '24,99 €', 'imagen': 'producto-generico.jpg', 'descripcion': 'Escayola 3D de alta calidad.'},
    ]
}

@product_bp.route("/productos/<categoria>")
def productos_categoria(categoria):
    productos_list = productos_por_categoria.get(categoria, [])
    return render_template("producto.html", categoria=categoria, productos=productos_list)

@product_bp.route("/producto/<producto_id>")
def producto(producto_id):
    producto = next((p for categoria in productos_por_categoria.values() for p in categoria if p["id"] == producto_id), None)
    if not producto:
        return "<h1>Producto no encontrado</h1>", 404
    return render_template("producto.html", producto=producto)
