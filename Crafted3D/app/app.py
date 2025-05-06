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
from forms.user_forms import RegistroUsuarioForm, LoginForm, ModificarContraseñaForm, CambiarContraseñaForm, EditarDireccionForm, EditarPerfilForm  

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    form = RegistroUsuarioForm()
    if request.method == 'POST' and form.validate_on_submit():
        flash("Registro exitoso. ¡Bienvenido!", "success")
        return redirect(url_for('inicio'))
    return render_template('registro.html', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        flash("Inicio de sesión exitoso!", "success")
        return redirect(url_for('perfil'))

    return render_template("login.html", form=form)

@app.route("/modificar_contraseña_1", methods=['GET', 'POST'])
def modificar_contraseña():
    form = ModificarContraseñaForm()
    if request.method == 'POST' and form.validate_on_submit():
        flash("Correo de recuperación enviado!", "success")
        return redirect(url_for('login'))

    return render_template("modificar_contraseña.html", form=form)

@app.route("/cambiar_contraseña", methods=['GET', 'POST'])
def cambiar_contraseña():
    form = CambiarContraseñaForm()
    if request.method == 'POST' and form.validate_on_submit():
        flash("Tu contraseña ha sido modificada!", "success")
        return redirect(url_for('login'))

    return render_template("cambiar_contraseña.html", form=form)

@app.route("/editar_direccion", methods=['GET', 'POST'])
def editar_direccion():
    form = EditarDireccionForm()
    if request.method == 'POST' and form.validate_on_submit():
        flash("Dirección actualizada correctamente!", "success")
        return redirect(url_for('perfil'))

    return render_template("editar_direccion.html", form=form)

@app.route("/editar_perfil", methods=['GET', 'POST'])
def editar_perfil():
    form = EditarPerfilForm()
    if request.method == 'POST' and form.validate_on_submit():
        flash("Perfil actualizado correctamente!", "success")
        return redirect(url_for('perfil'))

    return render_template("editar_perfil.html", form=form)









if __name__ == "__main__":
    app.run(debug=True)
