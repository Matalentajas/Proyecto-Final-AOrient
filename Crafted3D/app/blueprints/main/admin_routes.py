from flask import Blueprint, current_app, render_template, request, redirect, url_for, flash, session
import MySQLdb
from flask_login import current_user
from werkzeug.security import check_password_hash
from app.forms.admin_form import AdminLoginForm

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/admin", methods=["GET", "POST"])
def admin_login():
    
    if current_user.is_authenticated:
        flash("No tienes acceso al panel de administración.", "danger")
        return redirect(url_for("usuario.perfil"))

    if "admin" in session:
        return redirect(url_for("perfil_admin.html"))
    
    form = AdminLoginForm()

    if request.method == "POST" and form.validate_on_submit():
        email = form.email.data
        contraseña = form.contraseña.data

        #Consultar el administrador en la base de datos
        cursor = current_app.mysql.connection.cursor()
        cursor.execute("SELECT contraseña FROM administradores WHERE email = %s", (email,))
        admin_data = cursor.fetchone()
        cursor.close()

        if admin_data is None:
            #Si no se encuentra el administrador con ese correo
            form.email.errors.append("El correo electrónico no está registrado como administrador.")
        elif not check_password_hash(admin_data[0], contraseña):
            #Si la contraseña no es correcta
            form.contraseña.errors.append("La contraseña es incorrecta.")
        else:
            #Si las credenciales son correctas
            session["admin"] = email
            flash("Inicio de sesión exitoso, bienvenido al panel de administración!", "success")
            return redirect(url_for("admin.admin_dashboard"))

    return render_template("login_admin.html", form=form)

@admin_bp.route("/admin/dashboard")
def admin_dashboard():
    if "admin" not in session:
        flash("Debes iniciar sesión como administrador.", "danger")
        return redirect(url_for("admin.admin_login"))

    return render_template("perfil_admin.html")