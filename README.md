# Books API

Books API არის Django REST Framework-ზე დაწერილია პროექტი, სადაც შესაძლებელია საკუთარი წიგნების დამატება და მართვა.

მომხმარებელს შეუძლია რეგისტრაცია, ავტორიზაცია, პროფილის მართვა, წიგნების დამატება, რედაქტირება და წაშლა. ასევე შესაძლებელია წიგნის საჯაროდ გამოქვეყნება და სხვა მომხმარებლების საჯარო წიგნების შეფასება.

## Demo

Swagger:

https://books-api.ios.ge/api/docs/

Demo admin:

```text
Email: demo@admin.ge
Password: DemoAdmin123.
```

## გამოყენებული ტექნოლოგიები

- Python
- Django
- Django REST Framework
- Simple JWT
- drf-spectacular
- django-cors-headers
- WhiteNoise
- Gunicorn
- Docker
- SQLite

## ლოკალურად გაშვება

კლონირება:

```bash
git clone -b dev https://github.com/lasha94/books-api.git
cd books-api
```

Virtual environment:

```bash
python -m venv .venv
```

Linux / macOS:

```bash
source .venv/bin/activate
```

Windows:

```bash
.venv\Scripts\activate
```

პაკეტების დაყენება:

```bash
pip install -r requirements.txt
```

.env.example ფაილის მიხედვით შექმენი .env ან დააკოპირე:

Linux / macOS:

```bash
cp .env.example .env
```

Windows:

```bat
copy .env.example .env
```

Migration:

```bash
python manage.py migrate
```

superuser-ის შექმნა:

```bash
python manage.py createsuperuser
```

სერვერის გაშვება:

```bash
python manage.py runserver
```

API:

```text
http://127.0.0.1:8000/
```

Swagger:

```text
http://127.0.0.1:8000/api/docs/
```

Django Admin:

```text
http://127.0.0.1:8000/admin/
```

## Production

პროექტს აქვს `Dockerfile` და შესაძლებელია Docker-ით გაშვება.

Build:

```bash
docker build -t books-api .
```

Production გარემოსთვის საჭირო ცვლადები:

```env
SECRET_KEY=your-production-secret-key
DEBUG=False

ALLOWED_HOSTS=books-api.ios.ge
CSRF_TRUSTED_ORIGINS=https://books-api.ios.ge

DJANGO_SUPERUSER_EMAIL=admin@example.com
DJANGO_SUPERUSER_PHONE=+995500000000
DJANGO_SUPERUSER_PASSWORD=your-password
```

Container-ის გაშვება:

```bash
docker run -d \
  --name books-api \
  -p 8000:8000 \
  --env-file .env \
  books-api
```

Container-ის გაშვებისას ავტომატურად სრულდება migration და superadmin-ის შექმნა

პროექტი გაშვებულია Coolify-ის გარემოში.

Live API documentation:

https://books-api.ios.ge/api/docs/

## ძირითადი API

Authentication:

```text
POST /api/auth/register/
POST /api/auth/login/
POST /api/auth/logout/
POST /api/auth/token/refresh/

GET  /api/auth/profile/
PATCH /api/auth/profile/
```

Books:

```text
GET    /api/books/
POST   /api/books/

GET    /api/books/{id}/
PATCH  /api/books/{id}/
DELETE /api/books/{id}/
```

Public books:

```text
GET /api/books/public/
GET /api/books/public/{id}/
```

Reviews:

```text
GET  /api/books/public/{id}/reviews/
POST /api/books/public/{id}/reviews/
```

## ავტორი

Lasha Karaulashvili

GitHub:

https://github.com/lasha94
