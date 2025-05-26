# Importaciones necesarias de Flask, seguridad y formularios personalizados
from flask import Blueprint, current_app, render_template, request, redirect, url_for, flash, session
from flask_login import current_user
from werkzeug.security import check_password_hash
from app.forms.admin_form import AdminLoginForm, AgregarProductoForm, ProductoForm, CrearAdminForm
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash

# Definimos un Blueprint para agrupar las rutas del panel de administrador
admin_bp = Blueprint("admin", __name__)

# Ruta para el login del administrador
@admin_bp.route("/admin", methods=["GET", "POST"])
def admin_login():
    # Si el usuario está autenticado como usuario normal, lo redirigimos fuera del panel admin
    if current_user.is_authenticated:
        flash("No tienes acceso al panel de administración.", "danger")
        return redirect(url_for("usuario.perfil"))

    # Si ya hay sesión de admin, lo redirigimos al dashboard
    if "admin" in session:
        return redirect(url_for("admin.admin_dashboard"))

    form = AdminLoginForm()  # Instancia del formulario de login admin

    # Si el formulario se envió y es válido
    if form.validate_on_submit():
        email = form.email.data
        contraseña = form.contraseña.data

        # Buscar al admin en la base de datos
        cursor = current_app.mysql.connection.cursor()
        cursor.execute("SELECT contraseña FROM administradores WHERE email = %s", (email,))
        admin_data = cursor.fetchone()
        cursor.close()

        # Validaciones
        if admin_data is None:
            form.email.errors.append("El correo electrónico no está registrado como administrador.")
        elif not check_password_hash(admin_data[0], contraseña):
            form.contraseña.errors.append("La contraseña es incorrecta.")
        else:
            # Login correcto: guardar en sesión y redirigir al panel
            session["admin"] = email
            flash("Inicio de sesión exitoso, bienvenido al panel de administración!", "success")
            return redirect(url_for("admin.admin_dashboard"))

    # Renderizar el formulario de login
    return render_template("login_admin.html", form=form)

# Ruta para cerrar sesión como administrador
@admin_bp.route("/admin/logout")
def admin_logout():
    # Eliminar sesión admin y redirigir al login
    session.pop("admin", None)
    flash("Has cerrado sesión correctamente.", "success")
    return redirect(url_for("admin.admin_login"))

# Ruta del dashboard del admin
@admin_bp.route("/admin/dashboard")
def admin_dashboard():
    # Verificación de acceso
    if "admin" not in session:
        flash("Debes iniciar sesión como administrador para acceder a esta página.", "warning")
        return redirect(url_for("admin.admin_login"))
    return render_template("perfil_admin.html")  # Mostrar panel

# Ruta para agregar un nuevo producto
@admin_bp.route("/admin/agregar-producto", methods=["GET", "POST"])
def agregar_producto():
    if "admin" not in session:
        flash("Debes iniciar sesión como administrador.", "danger")
        return redirect(url_for("admin.admin_login"))

    form = AgregarProductoForm()

    # Obtener las categorías desde la base de datos
    cursor = current_app.mysql.connection.cursor()
    cursor.execute("SELECT id, nombre FROM categorias")
    categorias = cursor.fetchall()
    cursor.close()
    form.categoria_id.choices = [(c[0], c[1]) for c in categorias]  # Establecer opciones del select

    if form.validate_on_submit():
        # Recoger datos del formulario
        nombre = form.nombre_producto.data
        descripcion = form.descripcion.data
        precio = float(form.precio.data)
        imagenes = form.imagenes.data
        categoria_id = form.categoria_id.data

        # Insertar el producto en la base de datos
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

# Ruta para modificar productos existentes
@admin_bp.route("/admin/modificar_producto/", defaults={'producto_id': None}, methods=["GET", "POST"])
@admin_bp.route("/admin/modificar_producto/<int:producto_id>", methods=["GET", "POST"])
def modificar_producto(producto_id):
    form = ProductoForm()

    cursor = current_app.mysql.connection.cursor()

    # Obtener todos los productos y categorías
    cursor.execute("""
        SELECT p.id, p.nombre_producto, c.nombre, p.precio, p.imagenes
        FROM productos p
        JOIN categorias c ON p.categoria_id = c.id
    """)
    productos = cursor.fetchall()

    # Si se ha seleccionado un producto, obtener sus datos
    producto_seleccionado = None
    if producto_id is not None:
        cursor.execute("SELECT nombre_producto, descripcion, precio, categoria_id, imagenes FROM productos WHERE id = %s", (producto_id,))
        producto_seleccionado = cursor.fetchone()

    # Obtener categorías para el select del formulario
    cursor.execute("SELECT id, nombre FROM categorias")
    categorias = cursor.fetchall()
    form.categoria.choices = [(cat[0], cat[1]) for cat in categorias]

    cursor.close()

    # Rellenar el formulario con los datos del producto si es una solicitud GET
    if producto_seleccionado and request.method == "GET":
        form.nombre.data = producto_seleccionado[0]
        form.descripcion.data = producto_seleccionado[1]
        form.precio.data = producto_seleccionado[2]
        form.categoria.data = producto_seleccionado[3]
        form.imagen_url.data = producto_seleccionado[4]

    # Actualizar el producto en la base de datos si se envía el formulario
    if producto_seleccionado and request.method == "POST" and form.validate_on_submit():
        nuevo_nombre = form.nombre.data
        nueva_descripcion = form.descripcion.data
        nuevo_precio = form.precio.data
        nueva_categoria = form.categoria.data
        nueva_imagen_url = form.imagen_url.data

        cursor = current_app.mysql.connection.cursor()
        cursor.execute("""
            UPDATE productos SET nombre_producto=%s, descripcion=%s, precio=%s, categoria_id=%s, imagenes=%s WHERE id=%s
        """, (nuevo_nombre, nueva_descripcion, nuevo_precio, nueva_categoria, nueva_imagen_url, producto_id))
        current_app.mysql.connection.commit()
        cursor.close()

        flash("✅ Producto actualizado correctamente.", "success")
        return redirect(url_for("admin.modificar_producto", producto_id=producto_id))

    return render_template("modificar_producto.html", form=form, productos=productos, producto_seleccionado=producto_seleccionado)

# Ruta para eliminar un producto
@admin_bp.route("/admin/eliminar_producto/<int:producto_id>", methods=["POST"])
def eliminar_producto(producto_id):
    # Ejecutar la eliminación en la base de datos
    cursor = current_app.mysql.connection.cursor()
    cursor.execute("DELETE FROM productos WHERE id = %s", (producto_id,))
    current_app.mysql.connection.commit()
    cursor.close()
    flash("Producto eliminado correctamente.", "success")
    return redirect(url_for("admin.modificar_producto"))

# Ruta para ver lista de usuarios registrados
@admin_bp.route("/admin/usuarios", methods=["GET", "POST"])
def lista_usuarios():
    if "admin" not in session:
        flash("Debes iniciar sesión como administrador.", "danger")
        return redirect(url_for("admin.admin_login"))

    cursor = current_app.mysql.connection.cursor()

    # Obtener búsqueda si existe
    search_query = request.args.get('search', '')

    if search_query:
        # Buscar por nombre o correo
        query = """
            SELECT id, nombre_completo, email FROM usuarios
            WHERE nombre_completo LIKE %s OR email LIKE %s
            ORDER BY nombre_completo
        """
        like_pattern = f"%{search_query}%"
        cursor.execute(query, (like_pattern, like_pattern))
    else:
        cursor.execute("SELECT id, nombre_completo, email FROM usuarios ORDER BY nombre_completo")

    usuarios = cursor.fetchall()
    cursor.close()

    return render_template("lista_usuarios.html", usuarios=usuarios, search_query=search_query)

# Ruta para ver los pedidos de un usuario específico
@admin_bp.route("/admin/usuario/<int:usuario_id>/pedidos")
def ver_pedidos_usuario(usuario_id):
    if "admin" not in session:
        flash("Debes iniciar sesión como administrador.", "danger")
        return redirect(url_for("admin.admin_login"))

    cursor = current_app.mysql.connection.cursor()

    # Obtener datos del usuario
    cursor.execute("SELECT nombre_completo, email FROM usuarios WHERE id = %s", (usuario_id,))
    usuario = cursor.fetchone()

    if not usuario:
        flash("Usuario no encontrado.", "danger")
        cursor.close()
        return redirect(url_for("admin.lista_usuarios"))

    # Obtener pedidos de ese usuario
    cursor.execute("""
        SELECT numero_pedido, fecha_pedido, estado_pago, estado, total
        FROM pedidos
        WHERE usuario_id = %s
        ORDER BY fecha_pedido DESC
    """, (usuario_id,))
    pedidos = cursor.fetchall()
    cursor.close()

    return render_template("pedidos_usuario.html", usuario=usuario, pedidos=pedidos)

# Ruta para crear un nuevo administrador
@admin_bp.route("/admin/crear-admin", methods=["GET", "POST"])
def crear_admin():
    if "admin" not in session:
        flash("Debes iniciar sesión como administrador.", "danger")
        return redirect(url_for("admin.admin_login"))

    form = CrearAdminForm()

    if form.validate_on_submit():
        email = form.email.data
        contraseña = form.contraseña.data
        hashed_password = generate_password_hash(contraseña)  # Encriptar la contraseña

        cursor = current_app.mysql.connection.cursor()

        # Verificar si el email ya existe
        cursor.execute("SELECT id FROM administradores WHERE email = %s", (email,))
        existe = cursor.fetchone()

        if existe:
            flash("❌ Ya existe un administrador con ese correo.", "danger")
            cursor.close()
            return render_template("crear_admin.html", form=form)

        # Insertar el nuevo administrador
        cursor.execute(
            "INSERT INTO administradores (email, contraseña) VALUES (%s, %s)",
            (email, hashed_password)
        )
        current_app.mysql.connection.commit()
        cursor.close()

        flash("✅ Nuevo administrador creado correctamente.", "success")
        return redirect(url_for("admin.admin_dashboard"))

    return render_template("crear_admin.html", form=form)
