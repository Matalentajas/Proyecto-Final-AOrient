from flask import request
from wtforms import StringField, PasswordField, SubmitField, EmailField, DateField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo
from flask_wtf import FlaskForm
import re

# Función de validación manual de email
def validar_email_manual(email):
    patron = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(patron, email) is not None

# Formulario de Registro
class RegistroUsuarioForm(FlaskForm):
    nombre_completo = StringField('Nombre Completo', validators=[DataRequired(), Length(min=2, max=50)])
    email = EmailField('Correo Electrónico', validators=[DataRequired()])
    contraseña = PasswordField('Contraseña', validators=[DataRequired(), Length(min=6, max=150)])
    confirmar_contraseña = PasswordField('Confirmar Contraseña', validators=[
        DataRequired(),
        EqualTo('contraseña', message='Las contraseñas deben coincidir')
    ])
    fecha_nacimiento = DateField('Fecha de Nacimiento (Opcional)', format='%Y-%m-%d', validators=[])

    # Nuevos Campos
    direccion_completa = StringField('Dirección Completa', validators=[DataRequired(), Length(min=5, max=100)])
    ciudad = StringField('Ciudad', validators=[DataRequired(), Length(min=2, max=50)])
    codigo_postal = StringField('Código Postal', validators=[DataRequired(), Length(min=4, max=10)])

    submit = SubmitField('Registrarse')

    # Validación manual en `validate()`
    def validate(self, extra_validators=None):
        valid = super().validate(extra_validators=extra_validators)

        if request.method == "POST":
            # Validar formato de email
            if not validar_email_manual(self.email.data):
                self.email.errors = list(self.email.errors)
                self.email.errors.append("❌ El correo electrónico no es válido.")
                return False

            # Verificar si el correo ya está registrado
            import MySQLdb
            from flask import current_app

            conn = None
            cursor = None
            try:
                conn = MySQLdb.connect(
                    host=current_app.config['MYSQL_HOST'],
                    user=current_app.config['MYSQL_USER'],
                    passwd=current_app.config['MYSQL_PASSWORD'],
                    db=current_app.config['MYSQL_DB']
                )
                cursor = conn.cursor()
                cursor.execute("SELECT id FROM usuarios WHERE email = %s", (self.email.data,))
                if cursor.fetchone():
                    self.email.errors = list(self.email.errors)
                    self.email.errors.append("❌ Este correo ya está registrado.")
                    return False
            except Exception as e:
                print("Error al validar email en BD:", e)
            finally:
                if cursor is not None:
                    cursor.close()
                if conn is not None:
                    conn.close()

        return valid and not self.email.errors

# Formulario de Inicio de Sesión
class LoginForm(FlaskForm):
    email = EmailField('Correo Electrónico', validators=[DataRequired()])
    contraseña = PasswordField('Contraseña', validators=[DataRequired(), Length(min=6)])
    recordar_sesion = BooleanField('Recordar sesión')
    submit = SubmitField('Iniciar Sesión')

# Formulario de Recuperar Contraseña 1
class ModificarContraseñaForm(FlaskForm):
    email = EmailField('Dirección de email', validators=[DataRequired()])
    submit = SubmitField('Enviar Correo')

    def validate(self, extra_validators=None):
        valid = super().validate(extra_validators=extra_validators)

        if request.method == "POST":
            # Validar si el correo electrónico es válido
            if not validar_email_manual(self.email.data):
                if not self.email.errors:
                    self.email.errors = []
                else:
                    self.email.errors = list(self.email.errors)
                self.email.errors.append("❌ El correo electrónico no es válido.")
                return False

        return valid

# Formulario de Recuperar Contraseña 2
class CambiarContraseñaForm(FlaskForm):
    nueva_contraseña = PasswordField('Nueva Contraseña', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Cambiar Contraseña')

# Formulario de Editar Dirección
class EditarDireccionForm(FlaskForm):
    direccion_completa = StringField('Dirección Completa*', validators=[DataRequired(), Length(min=5, max=100)])
    codigo_postal = StringField('CP*', validators=[DataRequired(), Length(min=4, max=10)])
    ciudad = StringField('Ciudad*', validators=[DataRequired(), Length(min=2, max=50)])
    submit = SubmitField('Cambiar Dirección')

# Formulario de Editar Perfil
class EditarPerfilForm(FlaskForm):
    email = EmailField('Dirección de email*', validators=[DataRequired()])
    nombre = StringField('Nombre Completo*', validators=[DataRequired(), Length(min=2, max=50)])
    submit = SubmitField('Editar Perfil')

    def validate(self, extra_validators=None):
        valid = super().validate(extra_validators=extra_validators)

        if request.method == "POST":
            # Validar si el correo electrónico es válido
            if not validar_email_manual(self.email.data):
                if not self.email.errors:
                    self.email.errors = []
                else:
                    self.email.errors = list(self.email.errors)
                self.email.errors.append("❌ El correo electrónico no es válido.")
                return False

        return valid
