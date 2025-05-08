import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv
from app.config import Config
from flask_mysqldb import MySQL
from app.blueprints.main.order_routes import order_bp
from app.blueprints.main.product_routes import product_bp
from app.blueprints.main.user_routes import usuario_bp

# Cargar variables desde .env
load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)
app.register_blueprint(order_bp)
app.register_blueprint(product_bp)
app.register_blueprint(usuario_bp)

# Configurar la clave secreta desde .env
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Proteger los formularios contra ataques CSRF
csrf = CSRFProtect(app)

# Configuración de la BD
app.config["MYSQL_HOST"] = Config.MYSQL_HOST
app.config["MYSQL_USER"] = Config.MYSQL_USER
app.config["MYSQL_PASSWORD"] = Config.MYSQL_PASSWORD
app.config["MYSQL_DB"] = Config.MYSQL_DB

mysql = MySQL(app)
mysql.init_app(app)

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
