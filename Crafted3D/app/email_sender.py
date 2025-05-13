import smtplib
import os
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

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