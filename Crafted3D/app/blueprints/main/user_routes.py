from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.forms.user_forms import RegistroUsuarioForm, LoginForm, ModificarContraseñaForm, CambiarContraseñaForm, EditarDireccionForm, EditarPerfilForm  
from datetime import datetime
from werkzeug.security import generate_password_hash
from flask_mysqldb import MySQL

mysql = MySQL() 

usuario = {
    "nombre": "Juan Pérez",
    "direccion": "Calle Falsa 123",
    "codigo_postal": "28080",
    "ciudad": "Madrid",
    "pais": "España"
}

# Lista de pedidos de ejemplo
pedidos = [
    {
        "numero": "PED12345",
        "fecha": "2025-05-01",
        "estado_pago": "Pagado",
        "estado": "Completado",
        "total": 150.00
    },
    {
        "numero": "PED12346",
        "fecha": "2025-05-03",
        "estado_pago": "Procesando",
        "estado": "Enviado",
        "total": 75.50
    },
    {
        "numero": "PED12347",
        "fecha": "2025-05-05",
        "estado_pago": "Pendiente",
        "estado": "Cancelado",
        "total": 200.00
    }
]

usuario_bp = Blueprint("usuario", __name__)

#Vista del Perfil del usuario
@usuario_bp.route("/perfil")
def perfil():
    return render_template("perfil.html", usuario=usuario, pedidos=pedidos)


#Vista del formulario de registro
@usuario_bp.route('/registro', methods=['GET', 'POST'])
def registro():
    form = RegistroUsuarioForm()

    if request.method == 'POST' and form.validate_on_submit():
        nombre_completo = form.nombre_completo.data
        email = form.email.data
        contraseña = generate_password_hash(form.contraseña.data)
        direccion_completa = form.direccion_completa.data
        ciudad = form.ciudad.data
        codigo_postal = form.codigo_postal.data
        
        fecha_registro = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Guardamos la fecha para en el futuro usar un sistema de descuentos dependiendo de la antiguedad del cliente.

        cursor = mysql.connection.cursor()
        cursor.execute("""
            INSERT INTO usuarios (nombre_completo, email, contraseña, direccion_completa, ciudad, codigo_postal, fecha_registro) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (nombre_completo, email, contraseña, direccion_completa, ciudad, codigo_postal, fecha_registro))
        mysql.connection.commit()
        cursor.close()

        flash("Registro exitoso. ¡Bienvenido!", "success")
        return redirect(url_for('usuario.login'))

    return render_template('registro.html', form=form)








@usuario_bp.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        flash("Inicio de sesión exitoso!", "success")
        return redirect(url_for('usuario.perfil'))
    return render_template("login.html", form=form)

@usuario_bp.route("/modificar_contraseña_1", methods=['GET', 'POST'])
def modificar_contraseña():
    form = ModificarContraseñaForm()
    if request.method == 'POST' and form.validate_on_submit():
        flash("Correo de recuperación enviado!", "success")
        return redirect(url_for('usuario.login'))
    return render_template("modificar_contraseña.html", form=form)

@usuario_bp.route("/cambiar_contraseña", methods=['GET', 'POST'])
def cambiar_contraseña():
    form = CambiarContraseñaForm()
    if request.method == 'POST' and form.validate_on_submit():
        flash("Tu contraseña ha sido modificada!", "success")
        return redirect(url_for('usuario.login'))
    return render_template("cambiar_contraseña.html", form=form)

@usuario_bp.route("/editar_direccion", methods=['GET', 'POST'])
def editar_direccion():
    form = EditarDireccionForm()
    if request.method == 'POST' and form.validate_on_submit():
        flash("Dirección actualizada correctamente!", "success")
        return redirect(url_for('usuario.perfil'))
    return render_template("editar_direccion.html", form=form)

@usuario_bp.route("/editar_perfil", methods=['GET', 'POST'])
def editar_perfil():
    form = EditarPerfilForm()
    if request.method == 'POST' and form.validate_on_submit():
        flash("Perfil actualizado correctamente!", "success")
        return redirect(url_for('usuario.perfil'))
    return render_template("editar_perfil.html", form=form)
