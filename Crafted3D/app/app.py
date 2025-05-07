import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv
from config import Config
from models import db

# Cargar variables desde .env
load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

with app.app_context():
    db.create_all()

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
        "total": "29,99",
        "productos": [
            {"nombre": "Escayola 3D Modelo A", "cantidad": 2, "precio": "9,99 €"},
            {"nombre": "Caja Organizadora", "cantidad": 1, "precio": "10,00 €"}
        ]
    },
    {
        "numero": "ES789XYZ",
        "fecha": "15/03/2025",
        "estado_pago": "Pagado",
        "estado": "Completado",
        "total": "45,50",
        "productos": [
            {"nombre": "Escayola 3D Modelo B", "cantidad": 1, "precio": "24,99 €"},
            {"nombre": "Sistema Modular", "cantidad": 1, "precio": "18,99 €"}
        ]
    },
    {
        "numero": "ES123ABC",
        "fecha": "20/02/2025",
        "estado_pago": "Pagado",
        "estado": "Completado",
        "total": "60,99",
        "productos": [
            {"nombre": "Escayola 3D Modelo C", "cantidad": 1, "precio": "60,99 €"}
        ]
    },
    {
        "numero": "ES456DEF",
        "fecha": "01/01/2025",
        "estado_pago": "Pagado",
        "estado": "Completado",
        "total": "31,98",
        "productos": [
            {"nombre": "Caja Organizadora", "cantidad": 2, "precio": "12,99 €"},
            {"nombre": "Escayola 3D Modelo A", "cantidad": 1, "precio": "5,99 €"}
        ]
    }
]

pedido_actual = {
    "numero": "ES999XYZ",
    "fecha": "12/05/2025",
    "estado_pago": "Pendiente",
    "subtotal": "29,99",
    "envio": "5,00",
    "iva": "6,30",
    "total": "41,29",
    "productos": [
        {"nombre": "Escayola 3D Modelo A", "cantidad": 2, "precio": "9,99 €", "imagen": "producto-generico.jpg"},
        {"nombre": "Caja Organizadora", "cantidad": 1, "precio": "10,00 €", "imagen": "producto-generico.jpg"}
    ]
}

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

@app.route("/pedido/<numero>")
def pedido(numero):
    pedido = next((p for p in pedidos if p["numero"] == numero), None)

    if not pedido:
        flash("Pedido no encontrado.", "danger")
        return redirect(url_for("perfil"))

    return render_template("pedido.html", pedido=pedido)

@app.route("/confirmar_pedido", methods=['GET', 'POST'])
def confirmar_pedido():
    if request.method == 'POST':
        flash("Pedido confirmado con éxito!", "success")
        return redirect(url_for('pedido', numero=pedido_actual["numero"]))
    
    return render_template("confirmar_pedido.html", pedido=pedido_actual, usuario=usuario)




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
