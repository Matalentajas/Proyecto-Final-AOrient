import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf.csrf import CSRFProtect
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
login_manager.user_loader(load_user)  # ✅ Ahora solo está definido una vez

# Importar Blueprints después de inicializar `app`
from app.blueprints.main.order_routes import order_bp
from app.blueprints.main.product_routes import product_bp
from app.blueprints.main.user_routes import usuario_bp

# Registrar los Blueprints
app.register_blueprint(order_bp)
app.register_blueprint(product_bp)
app.register_blueprint(usuario_bp)

@app.route("/")
def index():
    db = conectar()
    cursor = db.cursor(DictCursor)
    
    cursor.execute("""
        SELECT id, nombre_producto AS nombre, descripcion, precio, imagenes AS imagen 
        FROM productos 
        WHERE categoria_id IN (
            SELECT id FROM categorias WHERE nombre IN ('Escayolas3D', 'Decoracion', 'Juguetes')
        )
        LIMIT 3
    """)
    productos_destacados = cursor.fetchall()
    
    cursor.close()
    db.close()

    return render_template("index.html", productos_destacados=productos_destacados)


@app.route("/test_db")
def test_db():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM usuarios")
    data = cursor.fetchall()
    cursor.close()
    return f"Usuarios en la BD: {data}"

if __name__ == "__main__":
    app.run(debug=True)
