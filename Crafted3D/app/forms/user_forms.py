from wtforms import StringField, PasswordField, SubmitField, EmailField, DateField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flask_wtf import FlaskForm

# Formulario de Registro
class RegistroUsuarioForm(FlaskForm):
    nombre = StringField('Nombre Completo', validators=[DataRequired(), Length(min=2, max=50)])
    email = EmailField('Correo Electrónico', validators=[DataRequired(), Email()])
    contraseña = PasswordField('Contraseña', validators=[DataRequired(), Length(min=6)])
    confirmar_contraseña = PasswordField('Confirmar Contraseña', validators=[
        DataRequired(),
        EqualTo('contraseña', message='Las contraseñas deben coincidir')
    ])
    fecha_nacimiento = DateField('Fecha de Nacimiento (Opcional)', format='%Y-%m-%d', validators=[])

    # Nuevos Campos
    direccion = StringField('Dirección Completa', validators=[DataRequired(), Length(min=5, max=100)])
    ciudad = StringField('Ciudad', validators=[DataRequired(), Length(min=2, max=50)])
    codigo_postal = StringField('Código Postal', validators=[DataRequired(), Length(min=4, max=10)])

    submit = SubmitField('Registrarse')

# Formulario de Inicio de Sesión
class LoginForm(FlaskForm):
    email = EmailField('Correo Electrónico', validators=[DataRequired(), Email()])
    contraseña = PasswordField('Contraseña', validators=[DataRequired(), Length(min=6)])
    recordar_sesion = BooleanField('Recordar sesión')
    submit = SubmitField('Iniciar Sesión')
