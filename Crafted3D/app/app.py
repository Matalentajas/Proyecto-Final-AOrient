import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf.csrf import CSRFProtect, generate_csrf
from dotenv import load_dotenv
from app.config import Config
from flask_mysqldb import MySQL
from flask_login import LoginManager
from app.models import load_user
from MySQLdb.cursors import DictCursor
from app.db import conectar

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Crear la instancia principal de la aplicación Flask
app = Flask(__name__)
# Cargar la configuración desde la clase Config
app.config.from_object(Config)

# Configurar la clave secreta para la aplicación (usada para sesiones y CSRF)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

# Inicializar protección CSRF para todos los formularios
csrf = CSRFProtect(app)

# Inyectar el token CSRF en el contexto de las plantillas para los formularios
@app.context_processor
def inject_csrf_token():
    return {"csrf_token": generate_csrf}

# Configuración de la base de datos MySQL usando variables de configuración
app.config["MYSQL_HOST"] = Config.MYSQL_HOST
app.config["MYSQL_USER"] = Config.MYSQL_USER
app.config["MYSQL_PASSWORD"] = Config.MYSQL_PASSWORD
app.config["MYSQL_DB"] = Config.MYSQL_DB

# Inicializar la extensión MySQL para Flask
mysql = MySQL(app)
app.mysql = mysql

# Inicializar el gestor de login de Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
# Especificar la vista de login por defecto
login_manager.login_view = "usuario.login"
# Registrar la función que carga un usuario desde la base de datos
login_manager.user_loader(load_user)

# Importar los Blueprints después de inicializar la aplicación
from app.blueprints.main.order_routes import order_bp
from app.blueprints.main.product_routes import product_bp
from app.blueprints.main.user_routes import usuario_bp
from app.blueprints.main.carrito_routes import carrito_bp
from app.blueprints.main.admin_routes import admin_bp

# Registrar los Blueprints en la aplicación principal
app.register_blueprint(carrito_bp)
app.register_blueprint(order_bp)
app.register_blueprint(product_bp)
app.register_blueprint(usuario_bp)
app.register_blueprint(admin_bp)

# Ruta principal de la aplicación (página de inicio)
@app.route("/")
def index():
    # Conectar a la base de datos
    db = conectar()
    cursor = db.cursor(DictCursor)
    
    # Consulta para obtener los 3 productos más destacados según la valoración media
    cursor.execute("""
        SELECT p.id, p.nombre_producto AS nombre, p.descripcion, p.precio, p.imagenes AS imagen,
               COALESCE((SELECT AVG(valor) FROM valoraciones WHERE producto_id = p.id), 0) AS media_valoracion
        FROM productos p
        ORDER BY media_valoracion DESC
        LIMIT 3
    """)
    productos_destacados = cursor.fetchall()
    
    # Cerrar el cursor y la conexión a la base de datos
    cursor.close()
    db.close()

    # Renderizar la plantilla index.html pasando los productos destacados
    return render_template("index.html", productos_destacados=productos_destacados)

# Función para manejar el error 404 (página no encontrada)
def error_404(error):
    return render_template('404.html')

# Registrar el manejador de errores para el error 404 en Flask
app.register_error_handler(404, error_404)

# Ejecutar la aplicación si este archivo es el principal
if __name__ == "__main__":
    app.run()
