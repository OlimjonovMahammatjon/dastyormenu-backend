# ✅ Railway Database Connection Muammosi Hal Qilindi!

## 🐛 Muammo

Railway da PostgreSQL ga ulanishda xatolik:
```
django.db.utils.OperationalError: connection failed: connection to server at "127.0.0.1", port 5432 failed: Connection refused
```

**Sabab**: Railway o'z `DATABASE_URL` environment variable dan foydalanadi, lekin Django settings buni qo'llab-quvvatlamagan edi.

## ✅ Yechim

### 1. dj-database-url Paketi Qo'shildi

`requirements.txt`:
```txt
dj-database-url==2.1.0
```

Bu paket `DATABASE_URL` ni avtomatik parse qiladi.

### 2. Settings Yangilandi

`config/settings/base.py`:
```python
import dj_database_url

DATABASE_URL = os.getenv('DATABASE_URL')
if DATABASE_URL:
    # Railway uses DATABASE_URL
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    # Local development
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('DB_NAME', 'dastyor_db'),
            'USER': os.getenv('DB_USER', 'postgres'),
            'PASSWORD': os.getenv('DB_PASSWORD', 'postgres'),
            'HOST': os.getenv('DB_HOST', 'localhost'),
            'PORT': os.getenv('DB_PORT', '5432'),
        }
    }
```

### 3. Start Script Yaratildi

`scripts/start.sh`:
```bash
#!/bin/bash
set -e

echo "Starting Dastyor Backend..."

# Wait for database to be ready
echo "Waiting for database..."
python << END
import sys
import time
import psycopg
from urllib.parse import urlparse
import os

max_tries = 30
tries = 0

DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    print("DATABASE_URL not set, skipping database check")
    sys.exit(0)

# Parse DATABASE_URL
url = urlparse(DATABASE_URL)
conn_params = {
    'dbname': url.path[1:],
    'user': url.username,
    'password': url.password,
    'host': url.hostname,
    'port': url.port or 5432
}

while tries < max_tries:
    try:
        conn = psycopg.connect(**conn_params)
        conn.close()
        print("Database is ready!")
        break
    except Exception as e:
        tries += 1
        print(f"Database not ready yet (attempt {tries}/{max_tries}): {e}")
        if tries >= max_tries:
            print("Could not connect to database after maximum retries")
            sys.exit(1)
        time.sleep(2)
END

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting server..."
daphne -b 0.0.0.0 -p ${PORT:-8000} config.asgi:application
```

**Afzalliklari**:
- ✅ Database tayyor bo'lishini kutadi (30 sekundgacha)
- ✅ Migrations avtomatik bajariladi
- ✅ Static files avtomatik yig'iladi
- ✅ Xatoliklar to'g'ri handle qilinadi

### 4. Railway Configuration Yangilandi

`railway.toml`:
```toml
[build]
builder = "NIXPACKS"

[deploy]
startCommand = "bash scripts/start.sh"
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 10
```

`Procfile`:
```
web: bash scripts/start.sh
worker: celery -A config worker -l info
beat: celery -A config beat -l info
```

## 🚀 Railway da Ishlash

### DATABASE_URL Format

Railway avtomatik ravishda `DATABASE_URL` yaratadi:
```
postgresql://user:password@host:port/database
```

Misol:
```
postgresql://postgres:password123@containers-us-west-123.railway.app:5432/railway
```

### Environment Variables

Railway da faqat `DATABASE_URL` kerak:
```bash
DATABASE_URL=${{Postgres.DATABASE_URL}}
```

Boshqa DB_* variables kerak emas, chunki `DATABASE_URL` dan parse qilinadi.

## 📋 Deploy Jarayoni

1. **Database Kutish** (0-30 sekund)
   - PostgreSQL tayyor bo'lishini kutadi
   - Har 2 sekundda retry qiladi
   - 30 sekunddan keyin timeout

2. **Migrations** (5-30 sekund)
   ```bash
   python manage.py migrate --noinput
   ```

3. **Static Files** (5-10 sekund)
   ```bash
   python manage.py collectstatic --noinput
   ```

4. **Server Start**
   ```bash
   daphne -b 0.0.0.0 -p $PORT config.asgi:application
   ```

## ✅ Test Qilish

### Local Test (DATABASE_URL bilan)

```bash
# DATABASE_URL o'rnatish
export DATABASE_URL="postgresql://postgres:password@localhost:5432/dastyor_db"

# Server ishga tushirish
python manage.py runserver

# Yoki start script bilan
bash scripts/start.sh
```

### Local Test (Oddiy)

```bash
# DATABASE_URL o'rnatilmagan bo'lsa, oddiy DB settings ishlatiladi
unset DATABASE_URL
python manage.py runserver
```

### Railway Test

Railway da avtomatik `DATABASE_URL` o'rnatiladi, hech narsa qilish kerak emas.

## 🔧 Troubleshooting

### 1. Database Connection Timeout

**Muammo**: 30 sekunddan keyin ham database tayyor emas

**Yechim**:
- Railway PostgreSQL service ishlab turganini tekshiring
- Railway dashboard da PostgreSQL logs ni ko'ring
- `DATABASE_URL` to'g'ri sozlanganini tekshiring

### 2. Migrations Fail

**Muammo**: Migrations bajarilmayapti

**Yechim**:
```bash
# Railway shell da
python manage.py migrate --noinput

# Yoki logs ni ko'ring
railway logs
```

### 3. Static Files 404

**Muammo**: Static files topilmayapti

**Yechim**:
```bash
# collectstatic bajarilganini tekshiring
python manage.py collectstatic --noinput

# WhiteNoise sozlanganini tekshiring (production.py)
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
```

### 4. Local Development

**Muammo**: Local da DATABASE_URL kerak emas

**Yechim**:
Settings avtomatik ravishda detect qiladi:
- `DATABASE_URL` mavjud bo'lsa → Railway mode
- `DATABASE_URL` yo'q bo'lsa → Local mode (DB_* variables)

## 📊 Railway Environment Variables

### Minimal Setup

Faqat shu kerak:
```bash
DATABASE_URL=${{Postgres.DATABASE_URL}}
REDIS_URL=${{Redis.REDIS_URL}}
SECRET_KEY=your-secret-key
DEBUG=False
DJANGO_SETTINGS_MODULE=config.settings.production
```

### To'liq Setup

```bash
# Django
SECRET_KEY=your-super-secret-key
DEBUG=False
DJANGO_SETTINGS_MODULE=config.settings.production
ALLOWED_HOSTS=.railway.app,yourdomain.com

# Database (Railway avtomatik)
DATABASE_URL=${{Postgres.DATABASE_URL}}

# Redis (Railway avtomatik)
REDIS_URL=${{Redis.REDIS_URL}}

# Celery
CELERY_BROKER_URL=${{Redis.REDIS_URL}}/0
CELERY_RESULT_BACKEND=${{Redis.REDIS_URL}}/0

# CORS & CSRF
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://your-app.railway.app
CSRF_TRUSTED_ORIGINS=https://yourdomain.com,https://your-app.railway.app

# Security
SECURE_SSL_REDIRECT=True

# App
BASE_URL=https://your-app.railway.app
PORT=8000
```

## 🎯 Natija

Barcha database muammolari hal qilindi:
- ✅ `DATABASE_URL` qo'llab-quvvatlanadi
- ✅ Database connection kutish logikasi
- ✅ Avtomatik migrations
- ✅ Avtomatik static files
- ✅ Local va Railway uchun universal
- ✅ Xatoliklar to'g'ri handle qilinadi

Railway ga deploy qilishga to'liq tayyor! 🚀

## 📚 Qo'shimcha Ma'lumot

### DATABASE_URL Format

```
postgresql://[user[:password]@][host][:port][/dbname][?param1=value1&...]
```

### dj-database-url Afzalliklari

- ✅ Avtomatik URL parsing
- ✅ Connection pooling support
- ✅ Health checks
- ✅ Multiple database backends
- ✅ Railway, Heroku, Render compatible

### Start Script Afzalliklari

- ✅ Database readiness check
- ✅ Graceful error handling
- ✅ Detailed logging
- ✅ Automatic retries
- ✅ Production-ready

Omad! 🎉
