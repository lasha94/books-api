FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn whitenoise

COPY manage.py .
COPY config/ config/
COPY accounts/ accounts/
COPY books/ books/

EXPOSE 8000

CMD python manage.py migrate --noinput \
    && python manage.py collectstatic --noinput \
    && python manage.py shell -c "import os; \
from django.contrib.auth import get_user_model; \
User = get_user_model(); \
email = os.environ['DJANGO_SUPERUSER_EMAIL'].strip().lower(); \
User.objects.filter(email__iexact=email).exists() or User.objects.create_superuser(email=email, phone=os.environ['DJANGO_SUPERUSER_PHONE'], password=os.environ['DJANGO_SUPERUSER_PASSWORD'])" \
    && exec gunicorn config.wsgi:application \
        --bind 0.0.0.0:8000 \
        --workers 1 \
        --access-logfile - \
        --error-logfile -