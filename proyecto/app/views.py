from django.shortcuts import render


def home_view(request):
    return render(request, "paginas/home.html",{})
def afterLogin(request):
    return render(request, "paginas/afterlogin.html",{})
def dashboard_view(request):
    return render(request,"paginas/dashboard.html",{})



# prueba para ver si funciona el correo
from django.http import HttpResponse
from correo.utils import enviar_correo_a_todos_los_usuarios

def prueba_envio_correo(request):
    asunto = "Prueba de envío de correo"
    mensaje = "Este es un correo de prueba enviado a todos los usuarios registrados en la plataforma."
    
    # Llamamos a la función para enviar el correo a todos los usuarios
    enviar_correo_a_todos_los_usuarios(asunto, mensaje)
    
    return HttpResponse("Correo de prueba enviado a todos los usuarios.")
