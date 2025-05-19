from wtforms import EmailField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length
from flask_wtf import FlaskForm

# Formulario de Inicio de Sesión para Administrador
class AdminLoginForm(FlaskForm):
    email = EmailField('Correo Electrónico', validators=[DataRequired()])
    contraseña = PasswordField('Contraseña', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Iniciar Sesión')
