FROM ghcr.io/railwayapp/nixpacks:python-3.11


# Instalar Python y dependencias del sistema
RUN apt-get update && \
    apt-get install -y python3 python3-pip build-essential libpq-dev && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Instalar dependencias de Python
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copiar el código
COPY . .

EXPOSE 8000

# Comando de arranque
CMD sh -c "python3 manage.py migrate --noinput && \
           python3 manage.py collectstatic --noinput && \
           daphne -b 0.0.0.0 -p ${PORT} BackGenAI.asgi:application"
