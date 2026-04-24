# 🚂 Railway Deployment Guide

## ✅ Muammolar Hal Qilindi

### 1. CORS Headers Qo'shildi
- ✅ `django-cors-headers==4.3.1` requirements.txt ga qo'shildi
- ✅ Production settings da CORS sozlandi

### 2. Static Files (WhiteNoise)
- ✅ `whitenoise==6.6.0` qo'shildi
- ✅ Static files xizmat qilish sozlandi

### 3. Production Server
- ✅ `gunicorn==21.2.0` qo'shildi (HTTP)
- ✅ `daphne==4.1.2` (ASGI/WebSocket)

## 🚀 Railway ga Deploy Qilish

### 1. Railway Project Yaratish

1. **Railway.app** ga kiring: https://railway.app
2. **New Project** tugmasini bosing
3. **Deploy from GitHub repo** ni tanlang
4. Repository ni tanlang

### 2. PostgreSQL Qo'shish

1. Project ichida **New** tugmasini bosing
2. **Database** → **PostgreSQL** ni tanlang
3. Database yaratiladi

### 3. Redis Qo'shish

1. **New** → **Database** → **Redis** ni tanlang
2. Redis yaratiladi

### 4. Environment Variables Sozlash

Railway dashboard da **Variables** bo'limiga o'ting va quyidagilarni qo'shing:

```bash
# Django
SECRET_KEY=your-super-secret-key-here-change-this
DEBUG=False
DJANGO_SETTINGS_MODULE=config.settings.production
ALLOWED_HOSTS=.railway.app,yourdomain.com

# Database (Railway PostgreSQL dan olinadi)
DATABASE_URL=${{Postgres.DATABASE_URL}}
DB_NAME=${{Postgres.PGDATABASE}}
DB_USER=${{Postgres.PGUSER}}
DB_PASSWORD=${{Postgres.PGPASSWORD}}
DB_HOST=${{Postgres.PGHOST}}
DB_PORT=${{Postgres.PGPORT}}

# Redis (Railway Redis dan olinadi)
REDIS_URL=${{Redis.REDIS_URL}}
REDIS_HOST=${{Redis.REDIS_HOST}}
REDIS_PORT=${{Redis.REDIS_PORT}}

# Celery
CELERY_BROKER_URL=${{Redis.REDIS_URL}}/0
CELERY_RESULT_BACKEND=${{Redis.REDIS_URL}}/0

# CORS & CSRF
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://your-app.railway.app
CSRF_TRUSTED_ORIGINS=https://yourdomain.com,https://your-app.railway.app

# Security
SECURE_SSL_REDIRECT=True

# S3 (Agar kerak bo'lsa)
USE_S3=False

# App
BASE_URL=https://your-app.railway.app
PORT=8000
```

### 5. Deploy Settings

Railway avtomatik ravishda `railway.toml` faylini o'qiydi:

```toml
[build]
builder = "NIXPACKS"

[deploy]
startCommand = "python manage.py migrate && python manage.py collectstatic --noinput && daphne -b 0.0.0.0 -p $PORT config.asgi:application"
```

### 6. Deploy Qilish

1. **Deploy** tugmasini bosing
2. Railway avtomatik build va deploy qiladi
3. Logs ni kuzating

## 📋 Deploy Jarayoni

Railway quyidagi buyruqlarni bajaradi:

1. **Dependencies o'rnatish**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Database migrations**:
   ```bash
   python manage.py migrate
   ```

3. **Static files yig'ish**:
   ```bash
   python manage.py collectstatic --noinput
   ```

4. **Server ishga tushirish**:
   ```bash
   daphne -b 0.0.0.0 -p $PORT config.asgi:application
   ```

## 🔧 Qo'shimcha Sozlamalar

### Custom Domain Qo'shish

1. Railway dashboard da **Settings** → **Domains**
2. **Custom Domain** qo'shing
3. DNS sozlamalarini yangilang

### Celery Worker (Alohida Service)

Celery worker uchun alohida service yarating:

1. **New** → **Empty Service**
2. Xuddi shu repository ni tanlang
3. Environment variables ni copy qiling
4. Start command ni o'zgartiring:
   ```bash
   celery -A config worker -l info
   ```

### Celery Beat (Alohida Service)

Periodic tasks uchun:

1. **New** → **Empty Service**
2. Start command:
   ```bash
   celery -A config beat -l info
   ```

## 🐛 Troubleshooting

### 1. ModuleNotFoundError

**Muammo**: `No module named 'corsheaders'`

**Yechim**: 
```bash
# requirements.txt da mavjudligini tekshiring
django-cors-headers==4.3.1
```

### 2. Static Files 404

**Muammo**: Static files topilmayapti

**Yechim**:
```bash
# collectstatic bajarilganini tekshiring
python manage.py collectstatic --noinput
```

### 3. Database Connection Error

**Muammo**: Database ga ulanish xatosi

**Yechim**:
- Railway PostgreSQL service ishlab turganini tekshiring
- Environment variables to'g'ri sozlanganini tekshiring
- `DATABASE_URL` o'rnatilganini tekshiring

### 4. CORS Errors

**Muammo**: Frontend dan API ga murojaat qilishda CORS xatosi

**Yechim**:
```python
# production.py da
CORS_ALLOWED_ORIGINS = [
    'https://yourdomain.com',
    'https://your-app.railway.app'
]
```

### 5. CSRF Token Errors

**Muammo**: CSRF verification failed

**Yechim**:
```python
# production.py da
CSRF_TRUSTED_ORIGINS = [
    'https://yourdomain.com',
    'https://your-app.railway.app'
]
```

## 📊 Monitoring

### Logs Ko'rish

Railway dashboard da **Deployments** → **View Logs**

### Database Monitoring

PostgreSQL service da **Metrics** bo'limini ko'ring

### Redis Monitoring

Redis service da **Metrics** bo'limini ko'ring

## 🔐 Security Checklist

- ✅ `DEBUG=False` production da
- ✅ `SECRET_KEY` o'zgartirilgan
- ✅ `ALLOWED_HOSTS` to'g'ri sozlangan
- ✅ `SECURE_SSL_REDIRECT=True`
- ✅ CORS va CSRF sozlangan
- ✅ Database credentials xavfsiz
- ✅ Static files WhiteNoise orqali

## 📚 Foydali Linklar

- **Railway Docs**: https://docs.railway.app
- **Django Deployment**: https://docs.djangoproject.com/en/stable/howto/deployment/
- **Daphne Docs**: https://github.com/django/daphne

## 🎯 Production Checklist

- [ ] PostgreSQL service yaratildi
- [ ] Redis service yaratildi
- [ ] Environment variables sozlandi
- [ ] `DJANGO_SETTINGS_MODULE=config.settings.production`
- [ ] `DEBUG=False`
- [ ] `SECRET_KEY` o'zgartirildi
- [ ] CORS va CSRF sozlandi
- [ ] Static files yig'ildi
- [ ] Migrations bajarildi
- [ ] Superuser yaratildi
- [ ] API test qilindi
- [ ] WebSocket test qilindi

## 🚀 Deploy Qilish Buyruqlari

### Local Test (Production Settings)

```bash
# Production settings bilan test
export DJANGO_SETTINGS_MODULE=config.settings.production
export DEBUG=False

# Static files
python manage.py collectstatic --noinput

# Migrations
python manage.py migrate

# Server
daphne -b 0.0.0.0 -p 8000 config.asgi:application
```

### Railway Deploy

```bash
# Git push qiling
git add .
git commit -m "Railway deployment ready"
git push origin main

# Railway avtomatik deploy qiladi
```

Omad! 🚀
