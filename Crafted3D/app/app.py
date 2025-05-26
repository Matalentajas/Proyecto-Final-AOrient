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

# Cargar variables desde .env
load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)

# Configurar la clave secreta desde .env
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

# Proteger los formularios contra ataques CSRF
csrf = CSRFProtect(app)
@app.context_processor
def inject_csrf_token():
    return {"csrf_token": generate_csrf}

# Configuración de la BD
app.config["MYSQL_HOST"] = Config.MYSQL_HOST
app.config["MYSQL_USER"] = Config.MYSQL_USER
app.config["MYSQL_PASSWORD"] = Config.MYSQL_PASSWORD
app.config["MYSQL_DB"] = Config.MYSQL_DB

mysql = MySQL(app)
app.mysql = mysql

# Inicializar Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "usuario.login"
login_manager.user_loader(load_user)

# Importar Blueprints después de inicializar `app`
from app.blueprints.main.order_routes import order_bp
from app.blueprints.main.product_routes import product_bp
from app.blueprints.main.user_routes import usuario_bp
from app.blueprints.main.carrito_routes import carrito_bp
from app.blueprints.main.admin_routes import admin_bp


#Registrar el Blueprint
app.register_blueprint(carrito_bp)
app.register_blueprint(order_bp)
app.register_blueprint(product_bp)
app.register_blueprint(usuario_bp)
app.register_blueprint(admin_bp)


@app.route("/")
def index():
    db = conectar()
    cursor = db.cursor(DictCursor)
    
    cursor.execute("""
        SELECT p.id, p.nombre_producto AS nombre, p.descripcion, p.precio, p.imagenes AS imagen,
               COALESCE((SELECT AVG(valor) FROM valoraciones WHERE producto_id = p.id), 0) AS media_valoracion
        FROM productos p
        ORDER BY media_valoracion DESC
        LIMIT 3
    """)
    productos_destacados = cursor.fetchall()
    
    cursor.close()
    db.close()

    return render_template("index.html", productos_destacados=productos_destacados)

#Pagina 404
def error_404(error):
    return render_template('404.html')

#Registramos en el manejador de errores el 404 en flask
app.register_error_handler(404,error_404)

if __name__ == "__main__":
    app.run(debug=True)
