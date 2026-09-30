# DRF JWT Auth

Django REST Framework project with a custom email-based `User` model, JWT authentication
(`djangorestframework-simplejwt`), and interactive API docs (`drf-spectacular` — Swagger UI + Redoc).

## Features

- Custom `User` model (`accounts.User`): email login instead of username, plus `phone_number`,
  `bio`, `date_of_birth`, `is_verified`, `created_at`, `updated_at`.
- JWT auth with access + refresh tokens, refresh rotation, and blacklisting on logout.
- Endpoints: register, login, logout, refresh, view/edit profile, change password, delete account.
- Password validation on register/change-password using Django's built-in validators
  (min length, common password, numeric-only, similarity to user attributes) plus password-confirmation matching.
- Swagger UI at `/api/docs/`, Redoc at `/api/redoc/`, raw OpenAPI schema at `/api/schema/`.

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # edit SECRET_KEY etc.
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Then open:
- Swagger UI: http://127.0.0.1:8000/api/docs/
- Redoc: http://127.0.0.1:8000/api/redoc/
- Admin: http://127.0.0.1:8000/admin/

Run tests with:

```bash
python manage.py test
```

## API Endpoints

All under `/api/auth/`.

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| POST | `/register/` | No | Create a new account |
| POST | `/login/` | No | Log in, returns `access` + `refresh` tokens and user profile |
| POST | `/logout/` | Yes | Blacklists the given `refresh` token |
| POST | `/token/refresh/` | No | Exchange a `refresh` token for a new `access` token |
| GET | `/profile/` | Yes | Get the authenticated user's profile |
| PUT/PATCH | `/profile/` | Yes | Update the authenticated user's profile |
| PUT | `/change-password/` | Yes | Change password (requires old password) |
| DELETE | `/delete/` | Yes | Permanently delete the account (requires current password) |

### Register

```bash
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
        "email": "jane@example.com",
        "first_name": "Jane",
        "last_name": "Doe",
        "password": "S3curePass!23",
        "password2": "S3curePass!23"
      }'
```

### Login

```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email": "jane@example.com", "password": "S3curePass!23"}'
```

Response includes `access`, `refresh`, and `user`. Send the access token as:

```
Authorization: Bearer <access_token>
```

### Logout

```bash
curl -X POST http://127.0.0.1:8000/api/auth/logout/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"refresh": "<refresh_token>"}'
```

### Update profile

```bash
curl -X PATCH http://127.0.0.1:8000/api/auth/profile/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"first_name": "Janet", "bio": "Hello world"}'
```

### Change password

```bash
curl -X PUT http://127.0.0.1:8000/api/auth/change-password/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"old_password": "S3curePass!23", "new_password": "EvenStr0nger!45", "new_password2": "EvenStr0nger!45"}'
```

### Delete account

```bash
curl -X DELETE http://127.0.0.1:8000/api/auth/delete/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"password": "EvenStr0nger!45"}'
```

## Notes

- `rest_framework_simplejwt.token_blacklist` is enabled so logout actually invalidates the refresh
  token server-side (otherwise a blacklisted-but-unexpired refresh token would still work).
- `DEFAULT_PERMISSION_CLASSES` is `IsAuthenticated` project-wide; register/login/refresh explicitly
  override this with `AllowAny`.
- Swap `SQLite` for Postgres/MySQL in `config/settings.py` `DATABASES` for production use, and set
  `DEBUG=False` with a real `SECRET_KEY` via `.env`.
