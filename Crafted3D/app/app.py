from flask import Flask, render_template

app = Flask(__name__)

# Categorías y productos
productos_por_categoria = {
    'escayolas3D': [
        {'nombre': 'Escayola 3D 1', 'precio': '19,99 €', 'imagen': 'producto-generico.jpg', 'descripcion': 'Una escayola 3D innovadora que transforma cualquier espacio con su diseño único.'},
        {'nombre': 'Escayola 3D 2', 'precio': '24,99 €', 'imagen': 'producto-generico.jpg', 'descripcion': 'Escayola 3D de alta calidad, ideal para proyectos de decoración modernos.'},
        {'nombre': 'Escayola 3D 1', 'precio': '19,99 €', 'imagen': 'producto-generico.jpg', 'descripcion': 'Una escayola 3D innovadora que transforma cualquier espacio con su diseño único.'},
        {'nombre': 'Escayola 3D 2', 'precio': '24,99 €', 'imagen': 'producto-generico.jpg', 'descripcion': 'Escayola 3D de alta calidad, ideal para proyectos de decoración modernos.'},
        {'nombre': 'Escayola 3D 1', 'precio': '19,99 €', 'imagen': 'producto-generico.jpg', 'descripcion': 'Una escayola 3D innovadora que transforma cualquier espacio con su diseño único.'},
        {'nombre': 'Escayola 3D 2', 'precio': '24,99 €', 'imagen': 'producto-generico.jpg', 'descripcion': 'Escayola 3D de alta calidad, ideal para proyectos de decoración modernos.'},
        {'nombre': 'Escayola 3D 1', 'precio': '19,99 €', 'imagen': 'producto-generico.jpg', 'descripcion': 'Una escayola 3D innovadora que transforma cualquier espacio con su diseño único.'},
        {'nombre': 'Escayola 3D 2', 'precio': '24,99 €', 'imagen': 'producto-generico.jpg', 'descripcion': 'Escayola 3D de alta calidad, ideal para proyectos de decoración modernos.'},
        {'nombre': 'Escayola 3D 2', 'precio': '24,99 €', 'imagen': 'producto-generico.jpg', 'descripcion': 'Escayola 3D de alta calidad, ideal para proyectos de decoración modernos.'},
    ],
    'almacenaje': [
        {'nombre': 'Almacenaje 1', 'precio': '12,99 €', 'imagen': 'producto-generico.jpg', 'descripcion': 'Caja de almacenaje versátil y resistente, perfecta para organizar tu hogar.'},
        {'nombre': 'Almacenaje 2', 'precio': '18,99 €', 'imagen': 'producto-generico.jpg', 'descripcion': 'Sistema de almacenaje modular que se adapta a tus necesidades.'},
    ],
    'herramientas': [
        {'nombre': 'Herramienta 1', 'precio': '9,99 €', 'imagen': 'producto-generico.jpg', 'descripcion': 'Herramienta multiusos compacta y duradera para cualquier tarea.'},
        {'nombre': 'Herramienta 2', 'precio': '15,99 €', 'imagen': 'producto-generico.jpg', 'descripcion': 'Herramienta profesional diseñada para trabajos de precisión.'},
    ],
    'gadgets': [
        {'nombre': 'Gadget 1', 'precio': '19,99 €', 'imagen': 'producto-generico.jpg', 'descripcion': 'Innovador gadget tecnológico que facilita tu día a día.'},
        {'nombre': 'Gadget 2', 'precio': '29,99 €', 'imagen': 'producto-generico.jpg', 'descripcion': 'Gadget de última generación con múltiples funciones avanzadas.'},
    ],
    'juguetes': [
        {'nombre': 'Juguete 1', 'precio': '12,99 €', 'imagen': 'producto-generico.jpg', 'descripcion': 'Juguete educativo que estimula la creatividad de los niños.'},
        {'nombre': 'Juguete 2', 'precio': '8,99 €', 'imagen': 'producto-generico.jpg', 'descripcion': 'Divertido juguete interactivo para horas de entretenimiento.'},
    ],
    'decoracion': [
        {'nombre': 'Decoración 1', 'precio': '25,99 €', 'imagen': 'producto-generico.jpg', 'descripcion': 'Elemento decorativo elegante que aporta estilo a cualquier espacio.'},
        {'nombre': 'Decoración 2', 'precio': '34,99 €', 'imagen': 'producto-generico.jpg', 'descripcion': 'Decoración moderna y sofisticada para realzar tus ambientes.'},
    ],
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/productos/<categoria>")
def productos(categoria):
    productos = productos_por_categoria.get(categoria, [])
    return render_template("productos.html", categoria=categoria, productos=productos)

if __name__ == "__main__":
    app.run(debug=True)

