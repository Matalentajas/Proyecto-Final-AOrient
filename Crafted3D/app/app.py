from flask import Flask, render_template

app = Flask(__name__)

# Datos unificados: Productos dentro de sus categorías
productos_por_categoria = {
    'escayolas3D': [
        {'id': 'escayola3D_01', 'nombre': 'Escayola 3D Modelo A', 'precio': '19,99 €', 'imagen': 'producto-generico.jpg', 'descripcion': 'Una escayola 3D innovadora que transforma cualquier espacio con su diseño único.'},
        {'id': 'escayola3D_02', 'nombre': 'Escayola 3D Modelo B', 'precio': '24,99 €', 'imagen': 'producto-generico.jpg', 'descripcion': 'Escayola 3D de alta calidad, ideal para proyectos de decoración modernos.'},
    ],
    'almacenaje': [
        {'id': 'almacenaje_01', 'nombre': 'Caja Organizadora', 'precio': '12,99 €', 'imagen': 'producto-generico.jpg', 'descripcion': 'Caja de almacenaje versátil y resistente, perfecta para organizar tu hogar.'},
        {'id': 'almacenaje_02', 'nombre': 'Sistema Modular', 'precio': '18,99 €', 'imagen': 'producto-generico.jpg', 'descripcion': 'Sistema de almacenaje modular que se adapta a tus necesidades.'},
    ],
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/productos/<categoria>")
def productos_categoria(categoria):
    productos_list = productos_por_categoria.get(categoria, [])
    return render_template("producto.html", categoria=categoria, productos=productos_list)

@app.route("/producto/<producto_id>")
def producto(producto_id):
    # Buscar el producto dentro de todas las categorías
    producto = next(
        (p for categoria in productos_por_categoria.values() for p in categoria if p["id"] == producto_id), None
    )
    if not producto:
        return "<h1>Producto no encontrado</h1>", 404
    return render_template("producto.html", producto=producto)

if __name__ == "__main__":
    app.run(debug=True)
