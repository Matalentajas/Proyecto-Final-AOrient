from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from app.forms.user_forms import RegistroUsuarioForm, LoginForm, ModificarContraseñaForm, CambiarContraseñaForm, EditarDireccionForm, EditarPerfilForm  
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from app.models import Usuario

usuario_bp = Blueprint("usuario", __name__)

# Lista de pedidos de ejemplo
pedidos = [
    {"numero": "PED12345", "fecha": "2025-05-01", "estado_pago": "Pagado", "estado": "Completado", "total": 150.00},
    {"numero": "PED12346", "fecha": "2025-05-03", "estado_pago": "Procesando", "estado": "Enviado", "total": 75.50},
    {"numero": "PED12347", "fecha": "2025-05-05", "estado_pago": "Pendiente", "estado": "Cancelado", "total": 200.00}
]

# Vista del perfil del usuario

@usuario_bp.route("/perfil")
@login_required  # ✅ Solo usuarios autenticados pueden ver su perfil
def perfil():
    cursor = current_app.mysql.connection.cursor()
    cursor.execute("SELECT nombre_completo, email, direccion_completa, ciudad, codigo_postal FROM usuarios WHERE id = %s", (current_user.id,))
    user_data = cursor.fetchone()
    cursor.close()

    if user_data:
        usuario_info = {
            "nombre_completo": user_data[0],
            "email": user_data[1],
            "direccion_completa": user_data[2],
            "ciudad": user_data[3],
            "codigo_postal": user_data[4],
        }
    else:
        usuario_info = None  # Si no se encuentra el usuario en la BD

    return render_template("perfil.html", usuario=usuario_info)

# Vista del formulario de registro con autenticación automática
@usuario_bp.route("/registro", methods=["GET", "POST"])
def registro():
    if current_user.is_authenticated:
        return redirect(url_for("usuario.perfil"))
    form = RegistroUsuarioForm()
    
    if request.method == "POST" and form.validate_on_submit():
        nombre_completo = form.nombre_completo.data
        email = form.email.data
        contraseña = generate_password_hash(form.contraseña.data)
        direccion_completa = form.direccion_completa.data
        ciudad = form.ciudad.data
        codigo_postal = form.codigo_postal.data
        
        cursor = current_app.mysql.connection.cursor()
        cursor.execute("""
            INSERT INTO usuarios (nombre_completo, email, contraseña, direccion_completa, ciudad, codigo_postal) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (nombre_completo, email, contraseña, direccion_completa, ciudad, codigo_postal))
        current_app.mysql.connection.commit()
        
        # Obtener el usuario recién registrado
        cursor.execute("SELECT id FROM usuarios WHERE email = %s", (email,))
        user_data = cursor.fetchone()
        cursor.close()

        if user_data:
            user_id = user_data[0]
            user = Usuario(user_id, nombre_completo, email)
            login_user(user)

        flash("Registro exitoso. ¡Bienvenido!", "success")
        return redirect(url_for("usuario.perfil"))

    return render_template("registro.html", form=form)

# Vista del login
@usuario_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("usuario.perfil"))
    form = LoginForm()
    
    if request.method == "POST" and form.validate_on_submit():
        email = form.email.data
        contraseña = form.contraseña.data

        cursor = current_app.mysql.connection.cursor()
        cursor.execute("SELECT id, nombre_completo, email, contraseña FROM usuarios WHERE email = %s", (email,))
        user_data = cursor.fetchone()
        cursor.close()

        if user_data and check_password_hash(user_data[3], contraseña):
            user = Usuario(user_data[0], user_data[1], user_data[2])
            login_user(user)
            flash("Inicio de sesión exitoso!", "success")
            return redirect(url_for("usuario.perfil"))
        else:
            flash("Correo o contraseña incorrectos", "danger")

    return render_template("login.html", form=form)


# Vista para modificar contraseña
@usuario_bp.route("/modificar_contraseña_1", methods=["GET", "POST"])
def modificar_contraseña():
    form = ModificarContraseñaForm()
    if request.method == "POST" and form.validate_on_submit():
        flash("Correo de recuperación enviado!", "success")
        return redirect(url_for("usuario.login"))
    return render_template("modificar_contraseña.html", form=form)

# Vista para cambiar contraseña
@usuario_bp.route("/cambiar_contraseña", methods=["GET", "POST"])
def cambiar_contraseña():
    form = CambiarContraseñaForm()
    if request.method == "POST" and form.validate_on_submit():
        flash("Tu contraseña ha sido modificada!", "success")
        return redirect(url_for("usuario.login"))
    return render_template("cambiar_contraseña.html", form=form)

# Vista para editar dirección del usuario
@usuario_bp.route("/editar_direccion", methods=["GET", "POST"])
@login_required
def editar_direccion():
    form = EditarDireccionForm(obj=current_user)

    if request.method == "POST" and form.validate_on_submit():
        direccion_completa = form.direccion_completa.data
        ciudad = form.ciudad.data
        codigo_postal = form.codigo_postal.data

        cursor = current_app.mysql.connection.cursor()
        cursor.execute("""
            UPDATE usuarios 
            SET direccion_completa = %s, ciudad = %s, codigo_postal = %s 
            WHERE id = %s
        """, (direccion_completa, ciudad, codigo_postal, current_user.id))
        current_app.mysql.connection.commit()
        cursor.close()

        flash("Dirección actualizada correctamente!", "success")
        return redirect(url_for("usuario.perfil"))

    return render_template("editar_direccion.html", form=form)



# Vista para editar los datos del usuario
@usuario_bp.route("/editar_perfil", methods=["GET", "POST"])
@login_required
def editar_perfil():
    form = EditarPerfilForm(obj=current_user)

    if request.method == "POST" and form.validate_on_submit():
        nombre_completo = form.nombre.data
        email = form.email.data

        cursor = current_app.mysql.connection.cursor()
        cursor.execute("""
            UPDATE usuarios 
            SET nombre_completo = %s, email = %s 
            WHERE id = %s   
        """, (nombre_completo, email, current_user.id))
        current_app.mysql.connection.commit()
        cursor.close()

        flash("Perfil actualizado correctamente!", "success")
        return redirect(url_for("usuario.perfil"))

    return render_template("editar_perfil.html", form=form)


#Cerrar la sesión del usuario
@usuario_bp.route("/logout")
@login_required
def logout():
    logout_user() 
    flash("Has cerrado sesión correctamente.", "info")
    return redirect(url_for("usuario.login"))