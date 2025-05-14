import secrets
from datetime import datetime, timedelta
from flask import current_app

def generar_token_recuperacion():
    return secrets.token_urlsafe(32)

def guardar_token(email):
    token = generar_token_recuperacion()
    expiracion = datetime.now() + timedelta(minutes=30)

    cursor = current_app.mysql.connection.cursor()
    cursor.execute("UPDATE usuarios SET reset_token = %s, reset_token_expiration = %s WHERE email = %s",
                   (token, expiracion, email))
    current_app.mysql.connection.commit()
    cursor.close()
    
    return token


def validar_token(token):
    cursor = current_app.mysql.connection.cursor()
    cursor.execute("SELECT email FROM usuarios WHERE reset_token = %s AND reset_token_expiration > NOW()", (token,))
    resultado = cursor.fetchone()
    cursor.close()
    
    return resultado is not None


def eliminar_token(email):
    cursor = current_app.mysql.connection.cursor()
    cursor.execute("UPDATE usuarios SET reset_token = NULL WHERE email = %s", (email,))
    current_app.mysql.connection.commit()
    cursor.close()

def limpiar_tokens_expirados():
    cursor = current_app.mysql.connection.cursor()
    cursor.execute("UPDATE usuarios SET reset_token = NULL, reset_token_expiration = NULL WHERE reset_token_expiration < NOW()")
    current_app.mysql.connection.commit()
    cursor.close()
