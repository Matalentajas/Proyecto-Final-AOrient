from wtforms import DecimalField, EmailField, PasswordField, SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, NumberRange, Optional, URL
from flask_wtf import FlaskForm


# Formulario de Inicio de Sesión para Administrador
class AdminLoginForm(FlaskForm):
    email = EmailField('Correo Electrónico', validators=[DataRequired()])
    contraseña = PasswordField('Contraseña', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Iniciar Sesión')

class AgregarProductoForm(FlaskForm):
    nombre_producto = StringField("Nombre del Producto", validators=[DataRequired(), Length(max=100)])
    descripcion = TextAreaField("Descripción", validators=[DataRequired()])
    precio = DecimalField("Precio", validators=[DataRequired(), NumberRange(min=0)])
    imagenes = StringField("URL de la Imagen", validators=[DataRequired(), Length(max=255)])
    categoria_id = SelectField("Categoría", coerce=int, validators=[DataRequired()])
    submit = SubmitField("Añadir Producto")

    
class ProductoForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    descripcion = TextAreaField('Descripción', validators=[DataRequired()])
    precio = DecimalField('Precio', validators=[DataRequired()])
    categoria = SelectField('Categoría', coerce=int, validators=[DataRequired()])
    imagen_url = StringField('URL de la imagen', validators=[Optional(), URL(message="Debe ser una URL válida")])    
    submit = SubmitField('Guardar Cambios')
