# Imagen base con Python 3.11
FROM python:3.11.9-slim-bullseye

# Establecer directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema (para psycopg2 y compilaciones)
RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

# Instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código del proyecto
COPY . .

# Exponer el puerto
EXPOSE 8000

# Comando de arranque
CMD sh -c "python manage.py migrate --noinput && \
           python manage.py collectstatic --noinput && \
           daphne -b 0.0.0.0 -p ${PORT} BackGenAI.asgi:application"
