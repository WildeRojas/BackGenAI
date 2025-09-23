web: python3 manage.py migrate --noinput && \
     python manage.py collectstatic --noinput && \
     daphne -b 0.0.0.0 -p $PORT BackGenAI.asgi:application
