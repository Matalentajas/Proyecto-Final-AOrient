from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import MySQLdb
from werkzeug.security import check_password_hash
from app.forms.admin_form import AdminLoginForm

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/admin", methods=["GET", "POST"])
def admin_login():
    form = AdminLoginForm()

    if request.method == "POST" and form.validate_on_submit():
        email = form.email.data
        contraseña = form.contraseña.data
        
        # 🚀 Conectar a la base de datos
        conn = MySQLdb.connect(
            host="TU_HOST",
            user="TU_USUARIO",
            passwd="TU_CONTRASEÑA",
            db="TU_BASE_DE_DATOS"
        )
        cursor = conn.cursor()

        # 🚀 Verificar credenciales de administrador
        cursor.execute("SELECT contraseña FROM administradores WHERE email = %s", (email,))
        admin_data = cursor.fetchone()
        
        cursor.close()
        conn.close()

        if admin_data and check_password_hash(admin_data[0], contraseña):
            session["admin"] = email  # ✅ Guardar sesión de admin
            flash("¡Bienvenido al panel de administración!", "success")
            return redirect(url_for("admin.dashboard"))
        else:
            flash("❌ Credenciales incorrectas. Inténtalo de nuevo.", "danger")

    return render_template("login_admin.html", form=form)

@admin_bp.route("/admin/dashboard")
def admin_dashboard():
    if "admin" not in session:
        flash("❌ Debes iniciar sesión como administrador.", "danger")
        return redirect(url_for("admin.admin_login"))
    
    return render_template("login_admin.html")
