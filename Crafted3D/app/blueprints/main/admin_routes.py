from flask import Blueprint, current_app, render_template, request, redirect, url_for, flash, session
from flask_login import current_user
from werkzeug.security import check_password_hash
from app.forms.admin_form import AdminLoginForm, AgregarProductoForm

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/admin", methods=["GET", "POST"])
def admin_login():
    if current_user.is_authenticated:
        flash("No tienes acceso al panel de administración.", "danger")
        return redirect(url_for("usuario.perfil"))

    if "admin" in session:
        return redirect(url_for("admin.admin_dashboard"))

    form = AdminLoginForm()

    if form.validate_on_submit():
        email = form.email.data
        contraseña = form.contraseña.data

        cursor = current_app.mysql.connection.cursor()
        cursor.execute("SELECT contraseña FROM administradores WHERE email = %s", (email,))
        admin_data = cursor.fetchone()
        cursor.close()

        if admin_data is None:
            form.email.errors.append("El correo electrónico no está registrado como administrador.")
        elif not check_password_hash(admin_data[0], contraseña):
            form.contraseña.errors.append("La contraseña es incorrecta.")
        else:
            session["admin"] = email
            flash("Inicio de sesión exitoso, bienvenido al panel de administración!", "success")
            return redirect(url_for("admin.admin_dashboard"))

    return render_template("login_admin.html", form=form)

@admin_bp.route("/admin/logout")
def admin_logout():
    session.pop("admin", None)
    flash("Has cerrado sesión correctamente.", "success")
    return redirect(url_for("admin.admin_login"))

@admin_bp.route("/admin/dashboard")
def admin_dashboard():
    if "admin" not in session:
        flash("Debes iniciar sesión como administrador para acceder a esta página.", "warning")
        return redirect(url_for("admin.admin_login"))
    return render_template("perfil_admin.html")


@admin_bp.route("/admin/agregar-producto", methods=["GET", "POST"])
def agregar_producto():
    if "admin" not in session:
        flash("Debes iniciar sesión como administrador.", "danger")
        return redirect(url_for("admin.admin_login"))

    form = AgregarProductoForm()

    # Obtener categorías desde la base de datos
    cursor = current_app.mysql.connection.cursor()
    cursor.execute("SELECT id, nombre FROM categorias")
    categorias = cursor.fetchall()
    cursor.close()
    form.categoria_id.choices = [(c[0], c[1]) for c in categorias]

    if form.validate_on_submit():
        nombre = form.nombre_producto.data
        descripcion = form.descripcion.data
        precio = float(form.precio.data)
        imagenes = form.imagenes.data
        categoria_id = form.categoria_id.data

        cursor = current_app.mysql.connection.cursor()
        cursor.execute("""
            INSERT INTO productos (nombre_producto, descripcion, precio, imagenes, fecha_creacion, categoria_id)
            VALUES (%s, %s, %s, %s, NOW(), %s)
        """, (nombre, descripcion, precio, imagenes, categoria_id))
        current_app.mysql.connection.commit()
        cursor.close()

        flash("Producto añadido correctamente.", "success")
        return redirect(url_for("admin.admin_dashboard"))

    return render_template("agregar_producto.html", form=form)


@admin_bp.route("/admin/modificar-producto")
def modificar_producto():
    return render_template("admin/modificar_producto.html")

@admin_bp.route("/admin/eliminar-producto")
def eliminar_producto():
    return render_template("admin/eliminar_producto.html")
