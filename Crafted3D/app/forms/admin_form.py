from wtforms import DecimalField, EmailField, PasswordField, SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, NumberRange, Optional, URL, EqualTo
from flask_wtf import FlaskForm
import re

# Formulario de Inicio de Sesión para Administrador
class AdminLoginForm(FlaskForm):
    email = EmailField('Correo Electrónico', validators=[DataRequired()])
    contraseña = PasswordField('Contraseña', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Iniciar Sesión')

# Formulario para Agregar Productos a la bd
class AgregarProductoForm(FlaskForm):
    nombre_producto = StringField("Nombre del Producto", validators=[DataRequired(), Length(max=100)])
    descripcion = TextAreaField("Descripción", validators=[DataRequired()])
    precio = DecimalField("Precio", validators=[DataRequired(), NumberRange(min=0)])
    imagenes = StringField("URL de la Imagen", validators=[DataRequired(), Length(max=255)])
    categoria_id = SelectField("Categoría", coerce=int, validators=[DataRequired()])
    submit = SubmitField("Añadir Producto")

# Formulario de Modificar Producto
class ProductoForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    descripcion = TextAreaField('Descripción', validators=[DataRequired()])
    precio = DecimalField('Precio', validators=[DataRequired()])
    categoria = SelectField('Categoría', coerce=int, validators=[DataRequired()])
    imagen_url = StringField('URL de la imagen', validators=[Optional(), URL(message="Debe ser una URL válida")])    
    submit = SubmitField('Guardar Cambios')

# Formulario de Crear un Administrador
class CrearAdminForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    contraseña = PasswordField('Contraseña', validators=[DataRequired(), Length(min=6)])
    confirmar_contraseña = PasswordField('Confirmar Contraseña', validators=[DataRequired(), EqualTo('contraseña')])
    submit = SubmitField('Crear Administrador')