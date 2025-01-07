from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.contrib.auth.models import User
from django.template.loader import render_to_string

# Función para enviar un correo simple
def enviar_correo_simple(asunto, mensaje, destinatarios):
    """
    Envía un correo simple a una lista de destinatarios.
    """
    send_mail(
        asunto, 
        mensaje, 
        settings.DEFAULT_FROM_EMAIL, 
        destinatarios
    )

# Función para enviar un correo HTML
def enviar_correo_html(asunto, contenido_html, destinatarios):
    """
    Envía un correo HTML a una lista de destinatarios.
    """
    email = EmailMessage(
        asunto, 
        contenido_html, 
        settings.DEFAULT_FROM_EMAIL, 
        destinatarios
    )
    email.content_subtype = "html"  # Especifica que el contenido es HTML
    email.send()

# Función para enviar un correo a todos los usuarios registrados
def enviar_correo_a_todos_los_usuarios(asunto, mensaje):
    """
    Envía un correo a todos los usuarios registrados en la base de datos.
    """
    usuarios = User.objects.all()  # Obtiene todos los usuarios
    destinatarios = [usuario.email for usuario in usuarios if usuario.email]  # Filtra los usuarios sin email
    
    if destinatarios:  # Solo envía si hay destinatarios
        enviar_correo_simple(asunto, mensaje, destinatarios)

# Función para enviar un correo con plantilla
def enviar_correo_con_plantilla(asunto, plantilla, context, destinatarios):
    """
    Envía un correo usando una plantilla de Django.
    """
    html_content = render_to_string(plantilla, context)
    email = EmailMessage(asunto, html_content, settings.DEFAULT_FROM_EMAIL, destinatarios)
    email.content_subtype = "html"
    email.send()

# Función para enviar un correo a todos los usuarios con plantilla
def enviar_correo_a_todos_los_usuarios_con_plantilla(asunto, plantilla, context):
    """
    Envía un correo con una plantilla a todos los usuarios registrados.
    """
    usuarios = User.objects.all()  # Obtiene todos los usuarios
    destinatarios = [usuario.email for usuario in usuarios if usuario.email]  # Filtra los usuarios sin email
    
    if destinatarios:  # Solo envía si hay destinatarios
        enviar_correo_con_plantilla(asunto, plantilla, context, destinatarios)
