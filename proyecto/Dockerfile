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
