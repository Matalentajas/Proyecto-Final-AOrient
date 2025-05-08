from flask_login import UserMixin
from flask import current_app

class Usuario(UserMixin):
    def __init__(self, id, nombre_completo, email):
        self.id = id
        self.nombre_completo = nombre_completo
        self.email = email

def load_user(user_id):
    cursor = current_app.mysql.connection.cursor()  # ✅ Usar `current_app.mysql` en vez de importación directa
    cursor.execute("SELECT id, nombre_completo, email FROM usuarios WHERE id = %s", (user_id,))
    user_data = cursor.fetchone()
    cursor.close()
    
    if user_data:
        return Usuario(*user_data)
    return None
