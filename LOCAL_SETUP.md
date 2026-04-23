# Dastyor Backend - Local Setup (Docker siz)

## ✅ O'rnatilgan Servislar

- ✅ PostgreSQL 15
- ✅ Redis
- ✅ Python 3.14 + Virtual Environment
- ✅ Django 6.0.4 (Python 3.14 compatible)
- ✅ Django REST Framework 3.17.1
- ✅ Barcha Python paketlar

## 🚀 Server Ishga Tushirish

### 1. Virtual Environment Faollashtirish
```bash
source venv/bin/activate
```

### 2. Django Server Ishga Tushirish
```bash
python manage.py runserver
```

Server manzili: **http://localhost:8000**

## 📋 Test Ma'lumotlar

### Admin Panel
- **URL**: http://localhost:8000/admin/
- **Username**: admin
- **Password**: admin123

### Test Organization
- **Name**: Test Restaurant
- **ID**: a8e97617-fda7-4230-bff0-856e61b672dd

### Test Users

#### Manager
- **Email**: manager@test.com
- **Password**: password123
- **Role**: manager

#### Chef
- **Email**: chef@test.com
- **Password**: password123
- **PIN**: 1234
- **Role**: chef

## 🔗 API Endpoints

### Swagger Documentation
http://localhost:8000/api/docs/

### API Schema
http://localhost:8000/api/schema/

### Admin Panel
http://localhost:8000/admin/

## 🧪 API Test Qilish

### 1. Login (Email/Password)
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "manager@test.com",
    "password": "password123"
  }'
```

**Response:**
```json
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "user": {
    "id": "...",
    "full_name": "Test Manager",
    "role": "manager"
  }
}
```

### 2. PIN Login (Chef/Waiter)
```bash
curl -X POST http://localhost:8000/api/auth/pin-login/ \
  -H "Content-Type: application/json" \
  -d '{
    "organization_id": "a8e97617-fda7-4230-bff0-856e61b672dd",
    "pin_code": "1234"
  }'
```

### 3. Organizations List (Auth kerak)
```bash
TOKEN="YOUR_ACCESS_TOKEN"

curl http://localhost:8000/api/organizations/ \
  -H "Authorization: Bearer $TOKEN"
```

### 4. Menu Yaratish
```bash
curl -X POST http://localhost:8000/api/menu/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Osh",
    "description": "Traditional Uzbek pilaf",
    "price": 2500000,
    "cook_time_minutes": 30,
    "is_available": true
  }'
```

### 5. Stol Yaratish
```bash
curl -X POST http://localhost:8000/api/tables/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "table_number": 1
  }'
```

## 🔧 Celery Ishga Tushirish (Alohida Terminal)

### Terminal 1: Celery Worker
```bash
source venv/bin/activate
celery -A config worker -l info
```

### Terminal 2: Celery Beat (Periodic Tasks)
```bash
source venv/bin/activate
celery -A config beat -l info
```

## 📊 Database Boshqarish

### PostgreSQL Shell
```bash
psql dastyor_db
```

### Django Shell
```bash
python manage.py shell
```

### Migratsiyalar
```bash
# Yangi migratsiya yaratish
python manage.py makemigrations

# Migratsiyalarni bajarish
python manage.py migrate

# Migratsiya holatini ko'rish
python manage.py showmigrations
```

## 🗄️ Redis Tekshirish

```bash
redis-cli ping
# Response: PONG

redis-cli
> KEYS *
> GET key_name
```

## 📝 Yangi Ma'lumot Qo'shish

### Django Shell orqali
```bash
python manage.py shell
```

```python
from apps.organizations.models import Organization
from apps.menu.models import Category, Menu
from apps.tables.models import Table

# Organization olish
org = Organization.objects.first()

# Category yaratish
category = Category.objects.create(
    organization=org,
    name="Main Dishes",
    icon="🍽️",
    sort_order=1
)

# Menu item yaratish
menu = Menu.objects.create(
    organization=org,
    category=category,
    name="Lag'mon",
    description="Hand-pulled noodles with meat and vegetables",
    price=2000000,  # 20,000 UZS (tiyin formatda)
    cook_time_minutes=25,
    is_available=True
)

# Stol yaratish
table = Table.objects.create(
    organization=org,
    table_number=1
)
print(f"QR Code ID: {table.qr_code_id}")
```

## 🔍 Debugging

### Server Loglarini Ko'rish
Server terminalda real-time ko'rinadi.

### Database Queries Debug
`config/settings/development.py` da:
```python
LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
```

## 🛠️ Muammolarni Hal Qilish

### Port band bo'lsa
```bash
# 8000 portni ishlatayotgan processni topish
lsof -i :8000

# Process ni to'xtatish
kill -9 PID
```

### PostgreSQL ishlamasa
```bash
# PostgreSQL holatini tekshirish
brew services list

# Qayta ishga tushirish
brew services restart postgresql@15
```

### Redis ishlamasa
```bash
# Redis holatini tekshirish
brew services list

# Qayta ishga tushirish
brew services restart redis
```

### Migration xatolari
```bash
# Barcha migratsiyalarni bekor qilish
python manage.py migrate APP_NAME zero

# Qayta migratsiya qilish
python manage.py migrate
```

### Database reset
```bash
# Database o'chirish
dropdb dastyor_db

# Qayta yaratish
createdb dastyor_db

# Migratsiyalar
python manage.py migrate

# Superuser
python manage.py createsuperuser
```

## 📚 Qo'shimcha Resurslar

- **API Documentation**: http://localhost:8000/api/docs/
- **Project Structure**: STRUCTURE.md
- **Full README**: README.md
- **Docker Setup**: docker-compose.yml

## 🎯 Keyingi Qadamlar

1. ✅ Server ishga tushdi
2. ✅ Test ma'lumotlar yaratildi
3. ✅ Login ishlayapti
4. 📝 Admin panel orqali ma'lumot qo'shing
5. 🧪 API endpointlarni test qiling
6. 🔌 WebSocket test qiling (Postman/wscat)
7. 📱 Frontend bilan integratsiya qiling

## 💡 Foydali Buyruqlar

```bash
# Virtual environment faollashtirish
source venv/bin/activate

# Server ishga tushirish
python manage.py runserver

# Yangi app yaratish
python manage.py startapp app_name

# Static fayllarni yig'ish
python manage.py collectstatic

# Test ishga tushirish
python manage.py test

# Database backup
pg_dump dastyor_db > backup.sql

# Database restore
psql dastyor_db < backup.sql
```

Omad! 🚀
