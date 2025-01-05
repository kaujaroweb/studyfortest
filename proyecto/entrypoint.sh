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
