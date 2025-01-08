## OBJETIVO : Explicar bien la base de la plantilla


Link para tener el ".env":

```
de momento mejor no ponerlo publico
```

## 1.PRIMER PASO
- Crear carpeta para el proyecto ( en este caso "plantilla")
- Dentro de ese directorio hacer 
```
django startproyect proyecto
```
- Cambiar el nombre de la aplicacion que se crea automaticamente a "app". Esta sera la aplicación central

## 2.SEGUNDO PASO
- Estando dentro de "plantilla", crear un .venv usando el comando 
```
python -m venv .venv
```
- Para activarlo:
C:\Users\GRA\Desktop\PROJECTS\plantilla>.venv\Scripts\activate

## 3.CREAR UN REQUIREMENTS.TXT
- Ahora estando dentro de "proyecto" crear un archivo que se llame "requirements.txt" con las siguientes cosas:
```
django
gunicorn
requests
django-dotenv
python-dotenv
psycopg2-binary
django-storages
boto3
django-tailwind
django-allauth
python-dotenv==1.0.1
whitenoise
PyJWT<3
cryptography
stripe
```
## 4.CREAR UN .ENV
- A la altura de "proyecto", crear un archivo ".env"
Este sirve para guardar todas las variables que no se van a subir a github

Copiar esto:
```
DEBUG=0
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_PASSWORD=guria
DJANGO_SUPERUSER_EMAIL=kaujaroweb@gmail.com
DJANGO_SECRET_KEY= luego_la_pongo

POSTGRES_READY= 1
POSTGRES_DB = dockerdc
POSTGRES_PASSWORD= guria_luego
POSTGRES_USER=guria
POSTGRES_HOST=postgres_db
POSTGRES_PORT=5432

REDIS_HOST= redis_db
REDIS_PORT=6380
```
## 5.CREAR REPOSITORIO DE GIT
- Estando en "plantilla" poner estos comandos:
```
git init
git add .
git commit m "Commit inicial"
git remote add origin git@github.com:kaujaroweb/plantilla.git
git push -u origin master
```
## 6.EMPEZAR A USAR EL .ENV
- Cambiar el wsgi.py de "app" para que entienda cual es su parent

```
import os
import pathlib
from dotenv import load_dotenv  # Corrected import for python-dotenv
from django.core.wsgi import get_wsgi_application

CURRENT_DIR = pathlib.Path(__file__).resolve().parent
BASE_DIR = CURRENT_DIR.parent
ENV_FILE_PATH = BASE_DIR / ".env"

    # Load environment variables from the .env file
load_dotenv(dotenv_path=str(ENV_FILE_PATH))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

application = get_wsgi_application()
```

- Cambiar el "manage.py" :
```
import os
import sys
from dotenv import load_dotenv  # Corrected import for python-dotenv


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    # Load environment variables from .env file
    load_dotenv()
    main()
```

## 7.EMPEZAR A CAMBIAR "settings.py" DE "app" para poder tener la base de datos POSTGRES SQL. ( https://www.youtube.com/watch?v=NAOsLaB6Lfc&t=6293s Min 42)

- Primero importar os al principio del todo de settings.py
```
import os
```
- Cambiar la secret key de django:

- Despues poner todo esto debajo de la base de datos por defecto
```
DB_USERNAME = os.environ.get("POSTGRES_USER")
DB_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
DB_DATABASE = os.environ.get("POSTGRES_DB")
DB_HOST = os.environ.get("POSTGRES_HOST")
DB_PORT = os.environ.get("POSTGRES_PORT")
DB_AVIAL = all([
    DB_USERNAME,
    DB_PASSWORD,
    DB_DATABASE,
    DB_HOST,
    DB_PORT
])


POSTGRES_READY= str(os.environ.get('POSTGRES_READY')) == "1"



if DB_AVIAL and POSTGRES_READY and True==False:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME":  DB_DATABASE,
            "USER": DB_USERNAME,
            "PASSWORD": DB_PASSWORD,
            "HOST": DB_HOST,
            "PORT":  DB_PORT,
        }
    }
```
## 8.PREPARAR STATIC FILES Y TEMPLATES PARA PREPARAR EL INSTALAR TAILWIND(PARA DESPUES PONERLO EN DOCKER TAMBIEN)
- Antes de nada crear un folder llamado "static" en proyecto (A la altura de manage.py) y este va a ser con el que va a funcionar todo. Depues va a haber otro folder fuera de esto que va a servir para cuando estemos en produccion y usemos "python manage.py collectstatic", cuando se ejecuta ese comando, se copia lo que tenemos en el "static" a esa otra carpeta. En este caso voy a llamar a esta carpeta de fuera "local-cdn/static" y esta a la altura de "proyecto" (fuera de el logicamente)
- Primero configurar las static files en settings.py
- Debajo de "STATIC_URL" hay que poner:
```
STATICFILES_DIRS = [BASE_DIR/ "static"]
STATIC_ROOT = BASE_DIR.parent / "local-cdn" / "static" # esto esta fuera de django y se usaria para produccion supuestamente
```
- Luego hay que ir a urls.py (de la app principal, en este caso "app"), y cambiarlo a esto:
```
import settings
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL,  document_root = settings.STATIC_ROOT)
```
- Para gestionar los templates hay que añadir "templates" a la parte de templates en "settings.py" en "DIRS"

### 8.2. Crear base.html y añadir un favicon.ico
- primero tener una imagen o un svg que queramos de favicon y llevarla a esta pagina:
```
https://www.svgviewer.dev/svg-to-png
```
- Dentro de proyecto, en "static" crear un nuevo folder llamado "img", y guardar ahi el favicon.ico (Antes de eso conseguir pasar de svg o imagen a favicon)
- Ahora en templates crear un base.html y un carpeta llamada "pages" para tener algo de html como ejemplo
```
{% load static %}
{% load socialaccount %}
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="icon" href="{% static 'img/favicon.ico' %}" type="image/x-icon">
    <link href="{% static 'css/output.css' %}" rel="stylesheet">
    <title>{% block title %}Guria Plantilla{% endblock %}</title>

</head>

<body>
    <div>
        {% block content %}
        <!-- Content will go here -->
        {% endblock %}
    </div>
    

</body>

</html>
```
- Añadir un views.py a "app"


## 9.INSTALAR TAILWIND A DJANGO
- Lo primero de todo es que el ordenador en el que se ejecuta esto tiene que tener "npm"
- Despues runnear este commando exacto fuera de "proyecto" es decir, a la misma altura que este
- 
```npm install -D tailwindcss 
```
--> esto crea una carpeta llamada "node_modules"
- Ahora runear 
```
npx tailwindcss init 
```
--> Esto crea el archivo tailwind.config.js. ** Muy importante meter el archivo dentro de proyecto despues de hacer esto**
- Despues de eso crear dentro de "static" (el de dentro de "proyecto") un folder que se llame "css" con un "input.css" y un "output.css"
- ahora en el "package.json" cambiarlo a esto: 
```
{
  "scripts":{
    "dev": "tailwindcss --i proyecto/static/css/input.css --o proyecto/static/css/output.css --watch"
  },
  "dependencies": {
    "tailwindcss": "^3.4.15"
  }
}
```
- Cambiar dentro de "input.css" poner esto: 
```
@tailwind base;
@tailwind components;
@tailwind utilities;
```
- Despues para runear esto y que se cambie ejecutar este comando (luego habra que ponerlo en el dockerfile)--> "npm run dev" (desde fuera de proyecto, a la misma altura que este)
- Casi acabando, ahora cada vez que se ponga codigo de tailwind en algun sitio, con el comando anterior se actualiza. Lo unico que falta es cambiar el "tailwind.config.json" para que detecte los archivos que tiene que cambiar, lo que hago con esto es solamente que dentro de proyecto, en cualquier folder, que cualquier archivo html o js lo detecte.
hay que poner esto dentro de tailwind.config.json "content" --> "./proyecto/**/*/{html,js}"

- Si no funciona el comando -->
```
npx run dev
```
- Estando en "proyecto" --> 
```
npx tailwindcss -o ./static/css/output.css
```



## 10.EMPEZAR CON DOCKER
- en la carpeta "proyecto" crear un ".dockerignore" y copiar lo mismo que habia en el gitignore
- ahora dentro de proyecto vamos a crear un dockerfile asi: (La explicacion de que hace cada cosa esta en el dockerfile)

```
# Usa una imagen base ligera de Python 3.11 para optimizar el tamaño del contenedor
FROM python:3.11-slim

# Establece variables de entorno para mejorar el comportamiento de Python
# Evita la creación de archivos .pyc
ENV PYTHONDONTWRITEBYTECODE=1
# Desactiva el buffering en la salida de Python
ENV PYTHONUNBUFFERED=1

# Instala dependencias del sistema necesarias para la aplicación y el frontend
# Incluye librerías para compilar extensiones de Python (como psycopg2),
# Node.js y npm para manejar dependencias frontend
RUN apt-get update && apt-get install -y \
    libpq-dev gcc \
    nodejs \
    npm && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Crea un entorno virtual de Python en /opt/venv para aislar dependencias
RUN python3 -m venv /opt/venv

# Asegura que el entorno virtual sea la versión de Python predeterminada
ENV PATH="/opt/venv/bin:$PATH"

# Define el directorio de trabajo donde se copiarán los archivos de la aplicación
WORKDIR /app

# Copia todos los archivos del proyecto local al contenedor
COPY . /app/

# Instala las dependencias de Python especificadas en requirements.txt
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Instala Tailwind CSS globalmente para usarlo como herramienta CLI
RUN npm install -g tailwindcss

# Compila el CSS de Tailwind para producción (optimizado y minificado)
RUN npx tailwindcss -i ./static/css/input.css -o ./static/css/output.css --minify

# Asegura que el script de entrada sea ejecutable
RUN chmod +x entrypoint.sh

# Define el script qu
CMD ["./entrypoint.sh"]
```

- Ahora hay que crear el archivo "entrypoint.sh"

```
#!/bin/bash

# Define el puerto en el que se ejecutará la aplicación
# Si no se ha establecido la variable de entorno PORT, usa el valor por defecto 8000
APP_PORT=${PORT:-8000}

# Cambia el directorio actual al directorio de trabajo de la aplicación
cd /app/

# Inicia el servidor Gunicorn con los siguientes parámetros:
# - Usa el entorno virtual de Python en /opt/venv/bin
# - Define un directorio temporal para los trabajadores en /dev/shm (memoria compartida para mejorar el rendimiento)
# - Especifica el archivo WSGI de la aplicación (irakasles.wsgi:application)
# - Liga el servidor al puerto definido (APP_PORT) en todas las interfaces de red (0.0.0.0)
# Esto asegura que la aplicación sea accesible desde fuera del contenedor.
exec /opt/venv/bin/gunicorn --worker-tmp-dir /dev/shm app.wsgi:application --bind "0.0.0.0:${APP_PORT}"

```
## 11.CREAR EL DOCKERCOMPOSE YAML
- Esto se crea para definir y ejecutar aplicaciones multi-contenedor con Docker. Vamos a crear un archivo llamado `docker-compose.yml` en el directorio raíz del proyecto.
- Fuera de "proyecto" se crea el archivo "docker-compose.yml"
```
services:
  web:
    depends_on:
      - postgres_db
    build:
      context: ./proyecto
      dockerfile: Dockerfile
    image: guria:latest
    ports:
      - "8000:8000"  # Map container port 8000 to host port 8000
    env_file:
      - proyecto/.env
    environment:
      - PORT:8000 # Example environment variable
    command: sh -c  "chmod +x /app/migrate.sh && sh /app/migrate.sh && /app/entrypoint.sh"

  postgres_db:
    image: postgres
    env_file:
      - proyecto/.env
    expose:
      - 5432
    volumes:
      - postgres_data:/var/lib/postgresql/data/  # Fixed volume as a list

volumes:
  postgres_data:  # Declare the named volume

```

- Para que funcione tambien hay que crear el archivo "migrate.sh" dentro de "proyecto":

```

#!/bin/bash

# Default email if DJANGO_SUPERUSER_EMAIL is not set
DJANGO_SUPERUSER_EMAIL=${DJANGO_SUPERUSER_EMAIL:-"kaujaroweb@gmail.com"}

# Change to the application directory
cd /app/

# Use Python from the virtual environment to run migrations
/opt/venv/bin/python manage.py migrate --noinput

# Create superuser if it doesn't exist
/opt/venv/bin/python manage.py createsuperuser --email $DJANGO_SUPERUSER_EMAIL --noinput || true
```

## 12.ALLAUTH PARA TENER LOGIN DE GOOGLE
- Hay que tener todo esto en settings.py

```

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
]

# allauth

AUTHENTICATION_BACKENDS = [
   
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by email
    'allauth.account.auth_backends.AuthenticationBackend',

]

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': os.environ.get("GOOGLE_CLIENT_ID"),
            'secret': os.environ.get("GOOGLE_CLIENT_SECRET"),
            'key': ''
        }
    }
}

ACCOUNT_USERNAME_REQUIRED = False  # No se requiere nombre de usuario
ACCOUNT_EMAIL_VERIFICATION = "mandatory"  # Verificación obligatoria de correo electrónico
ACCOUNT_EMAIL_REQUIRED = True  # Correo electrónico es obligatorio
SOCIAL_AUTH_GOOGLE_REDIRECT_URI = "http://172.20.10.2:8000/accounts/google/login/callback/"
SOCIALACCOUNT_AUTO_SIGNUP = True  # Crear automáticamente la cuenta si no existe
SOCIALACCOUNT_LOGIN_ON_GET = True  # Redirigir automáticamente después de la autenticación
LOGIN_REDIRECT_URL = 'after' # app datosUsuario


SITE_ID = 1  # Replace with the actual ID of your site in the admin panel




MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', #     WHITENOISE
    "allauth.account.middleware.AccountMiddleware", # django-allautgh
]

# allauth

```

- Despues de hacer eso hay que añadir esto a urls.py de "app":

```
path('accounts/', include('allauth.urls')),
```

## 13.CONFIGURACION PARA PODER MANDAR CORREOS

- Esto es para poder enviar correos desde Django. Para esto lo voy a configurar con gmail.

```
# Configuración del backend de correo
# Django utiliza un backend para enviar correos electrónicos. En este caso, usaremos el backend SMTP.
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

# Configuración del servidor SMTP de Gmail
EMAIL_HOST = "smtp.gmail.com"  # Dirección del servidor SMTP de Gmail
EMAIL_PORT = 587  # Puerto para conexión segura con TLS
EMAIL_USE_TLS = True  # Usar TLS (Transport Layer Security) para cifrar la conexión

# Credenciales de tu cuenta de Gmail
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")  # Tu dirección de correo de Gmail
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")  # Contraseña específica para aplicaciones

# Configuración del remitente por defecto
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER  # Dirección que aparecerá como remitente en los correos
```

- Para configurarlo en Gmail:

Habilita la autenticación en dos pasos:

Ve a tu Cuenta de Google.
En la sección de seguridad, activa la autenticación en dos pasos.
Genera una contraseña para aplicaciones:

Entra en la sección de Contraseñas de Aplicaciones (está en la misma página de seguridad).
Selecciona "Correo" como aplicación y "Otro" como dispositivo.
Copia la contraseña generada y úsala en EMAIL_HOST_PASSWORD.
Asegúrate de usar variables de entorno:

Para mantener seguras tus credenciales, no las escribas directamente en settings.py. En lugar de eso, usa un archivo .env y una librería como python-decouple o dotenv:


- Ejemplo de cómo enviar un correo
Enviar un correo simple:

```
from django.core.mail import send_mail

def enviar_correo_simple():
    send_mail(
        subject="Bienvenido a nuestra plataforma",
        message="Gracias por registrarte. Este es un correo de prueba.",
        from_email="tu_email@gmail.com",  # Puedes usar DEFAULT_FROM_EMAIL
        recipient_list=["destinatario@example.com"],
    )
```

Enviar un correo con HTML:
```
from django.core.mail import EmailMessage

def enviar_correo_html():
    asunto = "Tu pedido ha sido confirmado"
    mensaje_html = """
    <h1>¡Gracias por tu compra!</h1>
    <p>Tu pedido ha sido procesado con éxito.</p>
    """
    email = EmailMessage(asunto, mensaje_html, to=["destinatario@example.com"])
    email.content_subtype = "html"  # Especificar que el contenido es HTML
    email.send()
```

- Para hacer pruebas y que los correos no se manden, si no que se printeen en consola, hay que poner esto:
```
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
```

## 14.CREAR APP "CORREO" PARA PODER MANDAR GESTIONAR LA LOGICA DE MANDAR CORREOS DESE AHI

- Primero, esto se hace para modularizar la aplicacion y que las diferentes logicas esten separadas
- Desde dentro de "proyecto" en el cmd, escribir este comando:
```
python manage.py startapp correo

```
- Ahora en "app", settings.py meter la aplicacion "correo":

```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',

    # Aplicaciones propias
    'correo', # esta gestiona todo lo relacionado con correos
]

```

- Ahora dentro de "correo" crear un archivo "utils.py" en el cual van a ir las funciones para mandar correos

- Este es el codigo dentro de "correo" "utils.py", es codigo de prueba:
```
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

```
- Para comprobarlo tambien he creado una view en "app" views.py y la he añadido a urls.py. Asi he podido comprobar que funciona!


## 15.PLANTILLA SIMPLE PARA EL FRONTEND CON TAILWIND

- Primero cambiar tailwind para tener un "dark" mode. Para esto ir a "tailwind.config.js" y cambiarlo a esto:
```
// tailwind.config.js
/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class', // Use the class strategy for dark mode
  // other configurations...
}

```
- 

## 16.CREAR UNA APP PARA MANEJAR PAGOS CON STRIPE

- Lo primero, añadir a requirements.txt la libreria de stripe
```
django
gunicorn
requests
django-dotenv
psycopg2-binary
django-storages
boto3
django-tailwind
django-allauth
python-dotenv==1.0.1
whitenoise
PyJWT<3
cryptography
stripe
```

- Despues hay que hacerse una cuenta de Stripe y conseguir las claves ( voy a usar las de prueba y meterlas en el .env)

```
STRIPE_TEST_SECRET_KEY =claveprueba
STRIPE_TEST_PUBLIC_KEY =claveorueba
```
- Despues hay que crear una la app 

tengo que cambiar el requirements.txt del principio para meter stripe









