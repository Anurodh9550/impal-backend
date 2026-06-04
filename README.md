# IMPAL Food Backend (Django REST Framework)

Backend for the IMPAL Food Next.js project.

## Stack

- Django 5/6
- Django REST Framework
- JWT auth (`djangorestframework-simplejwt`)
- Neon Postgres via `DATABASE_URL`
- SQLite fallback for local testing

## Setup

```bash
cd "impaalfood/impal-food-backend"
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

Add your Neon Postgres URL in `.env`:

```env
DATABASE_URL=postgresql://USER:PASSWORD@HOST.neon.tech/DBNAME?sslmode=require
```

Then run:

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_impal
python manage.py runserver
```

API base:

```text
http://127.0.0.1:8000/api/
```

Admin panel:

```text
http://127.0.0.1:8000/admin/
```

## JWT Login

```http
POST /api/auth/token/
{
  "username": "admin",
  "password": "your-password"
}
```

Use returned access token:

```http
Authorization: Bearer <access>
```

## Main Endpoints

- `GET /api/products/`
- `POST /api/products/` admin only
- `GET /api/categories/`
- `GET /api/settings/current/`
- `POST /api/enquiries/` public contact form
- `GET /api/enquiries/` admin only
- `POST /api/orders/` public checkout
- `POST /api/orders/{id}/update_status/` admin only
- `GET /api/gallery/`
- `GET /api/testimonials/`
- `POST /api/upload/` admin only — multipart `file`, returns Cloudinary `{ url }`

## Cloudinary (image hosting)

1. Create a free account at https://cloudinary.com
2. From the dashboard copy the **API Environment variable** (`CLOUDINARY_URL`)
3. Paste it into `.env`:

```env
CLOUDINARY_URL=cloudinary://API_KEY:API_SECRET@CLOUD_NAME
```

Admin photo uploads from the Next.js admin panel are sent to `POST /api/upload/`,
stored in the `impal-food` folder on Cloudinary, and the returned secure URL is
saved on the product/gallery record.
