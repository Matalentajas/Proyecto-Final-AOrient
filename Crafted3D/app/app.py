import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv

# Cargar variables desde .env
load_dotenv()

app = Flask(__name__)

# Configurar la clave secreta desde .env
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Proteger los formularios contra ataques CSRF
csrf = CSRFProtect(app)

# Datos unificados: Productos dentro de sus categorías
productos_por_categoria = {
    'escayolas3D': [
        {'id': 'escayola3D_01', 'nombre': 'Escayola 3D Modelo A', 'precio': '19,99 €', 'imagen': 'producto-generico.jpg', 'descripcion': 'Una escayola 3D innovadora que transforma cualquier espacio con su diseño único.'},
        {'id': 'escayola3D_02', 'nombre': 'Escayola 3D Modelo B', 'precio': '24,99 €', 'imagen': 'producto-generico.jpg', 'descripcion': 'Escayola 3D de alta calidad, ideal para proyectos de decoración modernos.'},
        {'id': 'escayola3D_03', 'nombre': 'Escayola 3D Modelo C', 'precio': '60,99 €', 'imagen': 'producto-generico.jpg', 'descripcion': 'Escayola 3D de alta calidad, ideal para proyectos de decoración modernos.'},

    ],
    'almacenaje': [
        {'id': 'almacenaje_01', 'nombre': 'Caja Organizadora', 'precio': '12,99 €', 'imagen': 'producto-generico.jpg', 'descripcion': 'Caja de almacenaje versátil y resistente, perfecta para organizar tu hogar.'},
        {'id': 'almacenaje_02', 'nombre': 'Sistema Modular', 'precio': '18,99 €', 'imagen': 'producto-generico.jpg', 'descripcion': 'Sistema de almacenaje modular que se adapta a tus necesidades.'},
    ],

    'herramientas': [
        {'id': 'herramientas_01', 'nombre': 'Caja Organizadora', 'precio': '12,99 €', 'imagen': 'producto-generico.jpg', 'descripcion': 'Caja de almacenaje versátil y resistente, perfecta para organizar tu hogar.'},
        {'id': 'herramientas_02', 'nombre': 'Sistema Modular', 'precio': '18,99 €', 'imagen': 'producto-generico.jpg', 'descripcion': 'Sistema de almacenaje modular que se adapta a tus necesidades.'},
    ],
}

# Datos simulados de usuario
usuario = {
    "nombre": "Arturo",
    "direccion": "Calle Mayor 12, Valencia",
    "codigo_postal": "46001",
    "ciudad": "Valencia",
    "pais": "España"
}

# Historial de pedidos simulados
pedidos = [
    {
        "numero": "ES516QJK",
        "fecha": "09/04/2025",
        "estado_pago": "Pagado",
        "estado": "Enviado",
        "total": "9,99"
    },
    {
        "numero": "ES021QJK",
        "fecha": "01/04/2025",
        "estado_pago": "Pagado",
        "estado": "Completado",
        "total": "19,99"
    },
        {
        "numero": "ES516QJK",
        "fecha": "09/04/2025",
        "estado_pago": "Pagado",
        "estado": "Enviado",
        "total": "9,99"
    },
    {
        "numero": "ES021QJK",
        "fecha": "01/04/2025",
        "estado_pago": "Cancelado",
        "estado": "Cancelado",
        "total": "19,99"
    },
    {
        "numero": "ES516QJK",
        "fecha": "09/04/2025",
        "estado_pago": "Procesando",
        "estado": "Enviado",
        "total": "9,99"
    },
    {
        "numero": "ES021QJK",
        "fecha": "01/04/2025",
        "estado_pago": "Pagado",
        "estado": "Enviado",
        "total": "19,99"
    }
]

@app.route("/perfil")
def perfil():
    return render_template("perfil.html", usuario=usuario, pedidos=pedidos)

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



# Configuración de los formularios
from forms.user_forms import RegistroUsuarioForm

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    form = RegistroUsuarioForm()
    if request.method == 'POST' and form.validate_on_submit():
        flash("Registro exitoso. ¡Bienvenido!", "success")
        return redirect(url_for('inicio'))  # Redirigir a otra página después del registro
    return render_template('registro.html', form=form)










if __name__ == "__main__":
    app.run(debug=True)
