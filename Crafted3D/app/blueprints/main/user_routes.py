from flask import Blueprint, render_template, request, redirect, session, url_for, flash, current_app
from app.utils.token import guardar_token
from app.forms.user_forms import (
    RegistroUsuarioForm, LoginForm, ModificarContraseñaForm,
    CambiarContraseñaForm, EditarDireccionForm, EditarPerfilForm
)
from app.email_sender import (
    enviar_correo_bienvenida, enviar_correo_actualizacion,
    enviar_correo_actualizacion_direccion, enviar_correo_confirmacion,
    enviar_correo_recuperacion
)
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from app.models import Usuario
from datetime import timedelta

# Creamos un Blueprint para organizar rutas relacionadas con usuarios
usuario_bp = Blueprint("usuario", __name__)

# --- Vista perfil ---
@usuario_bp.route("/perfil")
@login_required  # Solo usuarios logueados pueden acceder
def perfil():
    # Si existe sesión admin, redirige al panel admin
    if "admin" in session:
        return redirect(url_for("admin.admin_dashboard"))

    cursor = current_app.mysql.connection.cursor()

    # Obtener datos del usuario
    cursor.execute("""
        SELECT nombre_completo, email, direccion_completa, ciudad, codigo_postal 
        FROM usuarios WHERE id = %s
    """, (current_user.id,))
    user_data = cursor.fetchone()

    usuario_info = {
        "nombre_completo": user_data[0],
        "email": user_data[1],
        "direccion_completa": user_data[2],
        "ciudad": user_data[3],
        "codigo_postal": user_data[4],
    } if user_data else None

    # Obtener pedidos reales desde la base de datos
    cursor.execute("""
        SELECT numero_pedido, fecha_pedido, estado_pago, estado, total 
        FROM pedidos 
        WHERE usuario_id = %s 
        ORDER BY fecha_pedido DESC
    """, (current_user.id,))
    pedidos_raw = cursor.fetchall()

    # Formatear pedidos para pasarlos al template

    pedidos = []
    for pedido in pedidos_raw:
        if pedido[0]:
            fecha_ajustada = pedido[1] + timedelta(hours=2) if pedido[1] else None
            pedidos.append({
                "numero": pedido[0],
                "fecha": fecha_ajustada.strftime("%Y-%m-%d %H:%M:%S") if fecha_ajustada else "",
                "estado_pago": pedido[2],
                "estado": pedido[3],
                "total": float(pedido[4])
            })

    cursor.close()

    return render_template("perfil.html", usuario=usuario_info, pedidos=pedidos)


# --- Registro de usuario ---
@usuario_bp.route("/registro", methods=["GET", "POST"])
def registro():
    # Si hay sesión de admin, redirige al panel admin
    if "admin" in session:
        return redirect(url_for("admin.admin_dashboard"))

    # Si usuario ya está autenticado, va a su perfil
    if current_user.is_authenticated:
        return redirect(url_for("usuario.perfil"))

    form = RegistroUsuarioForm()

    # Cuando se envía el formulario
    if request.method == "POST":
        print("Formulario recibido")

    if form.validate_on_submit():
        print("Formulario validado correctamente")

        # Extraemos datos del formulario
        nombre_completo = form.nombre_completo.data
        email = form.email.data
        contraseña = generate_password_hash(form.contraseña.data)
        direccion_completa = form.direccion_completa.data
        ciudad = form.ciudad.data
        codigo_postal = form.codigo_postal.data

        cursor = current_app.mysql.connection.cursor()

        # Insertamos usuario en la base de datos
        cursor.execute("""
            INSERT INTO usuarios (nombre_completo, email, contraseña, direccion_completa, ciudad, codigo_postal) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (nombre_completo, email, contraseña, direccion_completa, ciudad, codigo_postal))
        current_app.mysql.connection.commit()

        # Obtenemos id del usuario registrado
        cursor.execute("SELECT id FROM usuarios WHERE email = %s", (email,))
        user_data = cursor.fetchone()
        cursor.close()

        if user_data:
            user_id = user_data[0]
            user = Usuario(user_id, nombre_completo, email)
            login_user(user)  # Logueamos al usuario automáticamente

            print(f"📩 Intentando enviar correo de bienvenida a: {email}")
            enviar_correo_bienvenida(email, nombre_completo)
            print(f"Correo de bienvenida enviado con éxito.")

        return redirect(url_for("usuario.perfil"))

    else:
        print("Errores de validación:", form.errors)

    return render_template("registro.html", form=form)


# --- Login ---
@usuario_bp.route("/login", methods=["GET", "POST"])
def login():
    # Admin redirige a su panel
    if "admin" in session:
        return redirect(url_for("admin.admin_dashboard"))

    # Si ya está autenticado
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

        if user_data is None:
            form.email.errors.append("❌ El correo electrónico no está registrado.")
        elif not check_password_hash(user_data[3], contraseña):
            form.contraseña.errors.append("❌ La contraseña es incorrecta.")
        else:
            user = Usuario(user_data[0], user_data[1], user_data[2])
            login_user(user)
            flash("Inicio de sesión exitoso!", "success")
            return redirect(url_for("usuario.perfil"))

    return render_template("login.html", form=form)


# --- Modificar contraseña (paso 1: enviar correo) ---
@usuario_bp.route("/modificar_contraseña_1", methods=["GET", "POST"])
def modificar_contraseña():
    if "admin" in session:
        return redirect(url_for("admin.admin_dashboard"))

    form = ModificarContraseñaForm()

    if request.method == "POST" and form.validate_on_submit():
        email = form.email.data

        cursor = current_app.mysql.connection.cursor()
        cursor.execute("SELECT nombre_completo FROM usuarios WHERE email = %s", (email,))
        resultado = cursor.fetchone()
        cursor.close()

        if resultado:
            nombre = resultado[0]
            token = guardar_token(email)  # Crear token de recuperación
            enviar_correo_recuperacion(email, nombre, token)

            flash("Correo de recuperación enviado!", "success")
            return redirect(url_for("usuario.login"))
        else:
            flash("❌ El correo ingresado no está registrado.", "error")

    return render_template("modificar_contraseña.html", form=form)


# --- Cambiar contraseña (paso 2: con token) ---
@usuario_bp.route("/cambiar_contraseña/<token>", methods=["GET", "POST"])
def cambiar_contraseña(token):
    if "admin" in session:
        return redirect(url_for("admin.admin_dashboard"))

    form = CambiarContraseñaForm()

    cursor = current_app.mysql.connection.cursor()
    cursor.execute("SELECT email, nombre_completo FROM usuarios WHERE reset_token = %s", (token,))
    resultado = cursor.fetchone()
    cursor.close()

    if not resultado:
        return render_template("error.html", mensaje="❌ Token inválido o expirado.")

    email = resultado[0]
    nombre = resultado[1]

    if request.method == "POST" and form.validate_on_submit():
        nueva_contraseña = form.nueva_contraseña.data

        cursor = current_app.mysql.connection.cursor()
        nueva_contraseña_hash = generate_password_hash(nueva_contraseña)
        cursor.execute(
            "UPDATE usuarios SET contraseña = %s, reset_token = NULL WHERE email = %s",
            (nueva_contraseña_hash, email)
        )
        current_app.mysql.connection.commit()
        cursor.close()

        enviar_correo_confirmacion(email, nombre)
        return redirect(url_for("usuario.login", mensaje="✅ Contraseña actualizada exitosamente."))

    return render_template("cambiar_contraseña.html", form=form)


# --- Editar dirección ---
@usuario_bp.route("/editar_direccion", methods=["GET", "POST"])
@login_required
def editar_direccion():
    if "admin" in session:
        return redirect(url_for("admin.admin_dashboard"))

    form = EditarDireccionForm(obj=current_user)
    next_url = request.args.get("next", url_for("usuario.perfil"))

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

        enviar_correo_actualizacion_direccion(current_user.email, direccion_completa, ciudad, codigo_postal)
        return redirect(next_url)

    return render_template("editar_direccion.html", form=form, next_url=next_url)


# --- Editar perfil (nombre y email) ---
@usuario_bp.route("/editar_perfil", methods=["GET", "POST"])
@login_required
def editar_perfil():
    if "admin" in session:
        return redirect(url_for("admin.admin_dashboard"))

    form = EditarPerfilForm(obj=current_user)
    next_url = request.args.get("next", url_for("usuario.perfil"))

    if request.method == "POST" and form.validate_on_submit():
        nombre_completo = form.nombre.data  # corregido
        email = form.email.data

        cursor = current_app.mysql.connection.cursor()
        cursor.execute("""
            UPDATE usuarios 
            SET nombre_completo = %s, email = %s 
            WHERE id = %s
        """, (nombre_completo, email, current_user.id))
        current_app.mysql.connection.commit()
        cursor.close()

        enviar_correo_actualizacion(email, nombre_completo)
        return redirect(next_url)

    return render_template("editar_perfil.html", form=form, next_url=next_url)



# --- Logout ---
@usuario_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Has cerrado sesión correctamente.", "info")
    return redirect(url_for("usuario.login"))
