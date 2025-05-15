import smtplib
import os
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import url_for

load_dotenv()
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT"))
EMAIL_SENDER = os.getenv("MAIL_USERNAME")
EMAIL_PASSWORD = os.getenv("MAIL_PASSWORD")

def enviar_correo_bienvenida(destinatario, nombre):
    asunto = "¡Bienvenido a Crafted3D!"
    mensaje_html = f"""
    <html>
    <body>
        <h2>¡Hola {nombre}, bienvenido a Crafted3D! 🎉</h2>
        <p>Gracias por registrarte en nuestra plataforma.</p>
    </body>
    </html>
    """

    msg = MIMEMultipart()
    msg["From"] = EMAIL_SENDER
    msg["To"] = destinatario
    msg["Subject"] = asunto
    msg.attach(MIMEText(mensaje_html, "html"))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, destinatario, msg.as_string())
        server.quit()
        print("Correo enviado correctamente!")
    except Exception as e:
        print("Error al enviar correo:", e)

def enviar_correo_cambios_perfil(destinatario, nombre):
    asunto = "¡Bienvenido a Crafted3D!"
    mensaje_html = f"""
    <html>
    <body>
        <h2>¡Hola {nombre}, bienvenido a Crafted3D! 🎉</h2>
        <p>Gracias por registrarte en nuestra plataforma.</p>
    </body>
    </html>
    """

    msg = MIMEMultipart()
    msg["From"] = EMAIL_SENDER
    msg["To"] = destinatario
    msg["Subject"] = asunto
    msg.attach(MIMEText(mensaje_html, "html"))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, destinatario, msg.as_string())
        server.quit()
        print("Correo enviado correctamente!")
    except Exception as e:
        print("Error al enviar correo:", e)


def enviar_correo_actualizacion(destinatario, nombre):
    asunto = "¡Tus datos han sido actualizados!"
    mensaje_html = f"""
    <html>
    <body style="font-family: Arial, sans-serif; color: #333;">
        <h2>Hola {nombre},</h2>
        <p>Queremos informarte que los datos de tu cuenta han sido actualizados correctamente.</p>
        <p>Si tú hiciste estos cambios, no es necesario hacer nada más.</p>
        <p>Saludos,<br><strong>Equipo Crafted3D</strong></p>
    </body>
    </html>
    """

    msg = MIMEMultipart()
    msg["From"] = EMAIL_SENDER
    msg["To"] = destinatario
    msg["Subject"] = asunto
    msg.attach(MIMEText(mensaje_html, "html"))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, destinatario, msg.as_string())
        server.quit()
        print("Correo de actualización enviado correctamente!")
    except Exception as e:
        print("Error al enviar correo:", e)

def enviar_correo_actualizacion_direccion(destinatario, direccion, ciudad, codigo_postal):
    asunto = "¡Tu dirección ha sido actualizada!"
    mensaje_html = f"""
    <html>
    <body style="font-family: Arial, sans-serif; color: #333;">
        <h2>Hola,</h2>
        <p>Queremos informarte que tu dirección ha sido actualizada correctamente.</p>
        <p><strong>Nueva dirección:</strong><br>
        {direccion}, {ciudad}, {codigo_postal}</p>
        <p>Si tú hiciste estos cambios, no es necesario hacer nada más.</p>
        <p>Saludos,<br><strong>Equipo Crafted3D</strong></p>
    </body>
    </html>
    """

    msg = MIMEMultipart()
    msg["From"] = EMAIL_SENDER
    msg["To"] = destinatario
    msg["Subject"] = asunto
    msg.attach(MIMEText(mensaje_html, "html"))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, destinatario, msg.as_string())
        server.quit()
        print("✅ Correo de actualización de dirección enviado correctamente!")
    except Exception as e:
        print("❌ Error al enviar correo:", e)

    
def enviar_correo_recuperacion(destinatario, nombre, token):
    asunto = "Recuperación de Contraseña"
    enlace_recuperacion = url_for("usuario.cambiar_contraseña", token=token, _external=True)

    mensaje_html = f"""
    <html>
    <body style="font-family: Arial, sans-serif; color: #333;">
        <h2>Hola {nombre},</h2>
        <p>Has solicitado restablecer tu contraseña. Haz clic en el siguiente enlace para proceder:</p>
        <p><a href="{enlace_recuperacion}" style="color: #007bff; font-weight: bold;">Restablecer Contraseña</a></p>
        <p>Si no has solicitado este cambio, puedes ignorar este mensaje.</p>
        <p>Saludos,<br><strong>Equipo Crafted3D</strong></p>
    </body>
    </html>
    """

    msg = MIMEMultipart()
    msg["From"] = EMAIL_SENDER
    msg["To"] = destinatario
    msg["Subject"] = asunto
    msg.attach(MIMEText(mensaje_html, "html"))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, destinatario, msg.as_string())
        server.quit()
        print("✅ Correo de recuperación enviado correctamente!")
    except Exception as e:
        print("❌ Error al enviar correo de recuperación:", e)

def enviar_correo_confirmacion(destinatario, nombre):
    asunto = "Tu contraseña ha sido actualizada"
    
    mensaje_html = f"""
    <html>
    <body>
        <h2>Hola {nombre},</h2>
        <p>Queremos informarte que tu contraseña ha sido modificada exitosamente.</p>
        <p>Si no realizaste este cambio, por favor contacta con soporte de inmediato.</p>
        <p>Saludos,<br><strong>Equipo Crafted3D</strong></p>
    </body>
    </html>
    """
    
    msg = MIMEMultipart()
    msg["From"] = EMAIL_SENDER
    msg["To"] = destinatario
    msg["Subject"] = asunto
    msg.attach(MIMEText(mensaje_html, "html"))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, destinatario, msg.as_string())
        server.quit()
        print("✅ Correo de confirmación de cambio de contraseña enviado correctamente!")
    except Exception as e:
        print("❌ Error al enviar el correo de confirmación:", e)





def enviar_correo_confirmacion_pedido(destinatario, nombre, numero_pedido, pedido, direccion_completa, ciudad, codigo_postal):
    asunto = f"Confirmación de Pedido: {numero_pedido}"

    
    mensaje_html = f"""
    <html>
    <body style="font-family: Arial, sans-serif; color: #333;">
        <h2>¡Hola {nombre}, tu pedido ha sido confirmado! 🎉</h2>
        <p>Gracias por tu compra. Aquí tienes los detalles de tu pedido:</p>
        <p><strong>Número de Pedido:</strong> {numero_pedido}</p>
        <p><strong>Dirección de envío:</strong> {direccion_completa}, {ciudad}, {codigo_postal}</p>

        <h3>Productos comprados:</h3>
        <ul>
    """
    print("DEBUG - pedido:", pedido)
    for producto in pedido["productos"]:
        mensaje_html += f"<li>{producto['nombre']} | Cantidad: {producto['cantidad']} | Total: {producto['precio_total']} €</li>"

    mensaje_html += f"""
        </ul>

        <p><strong>Total con IVA:</strong> {float(pedido['total']) * 1.21:.2f} €</p>

        <h3>Seguimiento de Pedido:</h3>
        <p><a href="https://seguimiento-falso.com/{numero_pedido}" style="color: #007bff; font-weight: bold;">
        Haz clic aquí para ver el estado de tu pedido</a></p>

        <p>¡Gracias por confiar en Crafted3D! 🙌</p>
    </body>
    </html>
    """

    #Configurar y enviar el correo
    msg = MIMEMultipart()
    msg["From"] = EMAIL_SENDER
    msg["To"] = destinatario
    msg["Subject"] = asunto
    msg.attach(MIMEText(mensaje_html, "html"))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, destinatario, msg.as_string())
        server.quit()
        print(f"✅ Correo de confirmación de pedido ({numero_pedido}) enviado correctamente!")
    except Exception as e:
        print(f"❌ Error al enviar el correo de confirmación de pedido: {e}")

        
