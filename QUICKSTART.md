# Dastyor Backend - Quick Start Guide

## 🚀 Tezkor Boshlash (Docker bilan)

### 1. Loyihani Klonlash
```bash
cd DastyorMenuBackend
```

### 2. Environment O'rnatish
```bash
cp .env.example .env
# .env faylini tahrirlang (kerak bo'lsa)
```

### 3. Docker Containerlarni Ishga Tushirish
```bash
docker-compose up -d
```

Bu quyidagi servislarni ishga tushiradi:
- **PostgreSQL** (port 5432)
- **Redis** (port 6379)
- **MinIO** (port 9000, 9001)
- **Django Web** (port 8000)
- **Celery Worker**
- **Celery Beat**

### 4. Migratsiyalarni Bajarish
```bash
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
```

### 5. Superuser Yaratish
```bash
docker-compose exec web python manage.py createsuperuser
```

### 6. API ni Tekshirish
- **API Root**: http://localhost:8000/api/
- **Swagger Docs**: http://localhost:8000/api/docs/
- **Admin Panel**: http://localhost:8000/admin/

## 📋 Makefile Buyruqlari

```bash
make help              # Barcha buyruqlarni ko'rish
make build             # Docker image yaratish
make up                # Servislarni ishga tushirish
make down              # Servislarni to'xtatish
make logs              # Loglarni ko'rish
make shell             # Django shell ochish
make migrate           # Migratsiyalarni bajarish
make makemigrations    # Migratsiyalar yaratish
make createsuperuser   # Superuser yaratish
```

## 🧪 Test Qilish

### 1. Organization Yaratish
```bash
curl -X POST http://localhost:8000/api/organizations/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Restaurant",
    "phone": "+998901234567",
    "address": "Tashkent, Uzbekistan"
  }'
```

### 2. User Yaratish
```bash
curl -X POST http://localhost:8000/api/users/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "John Chef",
    "role": "chef",
    "email": "chef@test.com",
    "password": "password123",
    "pin_code": "1234"
  }'
```

### 3. Login (Email/Password)
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "chef@test.com",
    "password": "password123"
  }'
```

### 4. Login (PIN)
```bash
curl -X POST http://localhost:8000/api/auth/pin-login/ \
  -H "Content-Type: application/json" \
  -d '{
    "organization_id": "YOUR_ORG_ID",
    "pin_code": "1234"
  }'
```

### 5. Menu Yaratish
```bash
curl -X POST http://localhost:8000/api/menu/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Osh",
    "description": "Traditional Uzbek pilaf",
    "price": 2500000,
    "cook_time_minutes": 30,
    "is_available": true
  }'
```

### 6. Stol Yaratish
```bash
curl -X POST http://localhost:8000/api/tables/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "table_number": 1
  }'
```

### 7. Public Menu Olish (QR orqali)
```bash
curl http://localhost:8000/api/public/menu/?qr=QR_CODE_ID
```

### 8. Buyurtma Berish (Mijoz)
```bash
curl -X POST http://localhost:8000/api/public/orders/ \
  -H "Content-Type: application/json" \
  -d '{
    "qr_code_id": "QR_CODE_ID",
    "customer_note": "No onions please",
    "items": [
      {
        "menu": "MENU_ID",
        "quantity": 2,
        "modifications": "Extra spicy"
      }
    ]
  }'
```

## 🔌 WebSocket Test

### Orders WebSocket
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/orders/?token=YOUR_ACCESS_TOKEN');

ws.onopen = () => {
  console.log('Connected to orders');
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Order update:', data);
};
```

### Notifications WebSocket
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/notifications/?token=YOUR_ACCESS_TOKEN');

ws.onopen = () => {
  console.log('Connected to notifications');
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Notification:', data);
};
```

## 🐛 Debugging

### Loglarni Ko'rish
```bash
# Barcha servislar
docker-compose logs -f

# Faqat web
docker-compose logs -f web

# Faqat celery
docker-compose logs -f celery
```

### Django Shell
```bash
docker-compose exec web python manage.py shell
```

```python
# Test organization yaratish
from apps.organizations.models import Organization
org = Organization.objects.create(name="Test Cafe")

# Test user yaratish
from django.contrib.auth.models import User
from apps.users.models import UserProfile
user = User.objects.create_user('test', 'test@test.com', 'pass')
profile = UserProfile.objects.create(
    user=user,
    organization=org,
    full_name="Test User",
    role="manager"
)
```

### Database Shell
```bash
docker-compose exec postgres psql -U postgres -d dastyor_db
```

## 📊 Monitoring

### Redis CLI
```bash
docker-compose exec redis redis-cli
```

### MinIO Console
http://localhost:9001/
- Username: minioadmin
- Password: minioadmin

## 🔧 Troubleshooting

### Port band bo'lsa
```bash
# Portlarni tekshirish
lsof -i :8000
lsof -i :5432
lsof -i :6379

# Servislarni to'xtatish
docker-compose down
```

### Database reset
```bash
docker-compose down -v
docker-compose up -d
docker-compose exec web python manage.py migrate
```

### Celery ishlamasa
```bash
docker-compose restart celery celery-beat
docker-compose logs -f celery
```

## 📚 Qo'shimcha Ma'lumot

- **API Documentation**: http://localhost:8000/api/docs/
- **Admin Panel**: http://localhost:8000/admin/
- **Project Structure**: STRUCTURE.md
- **Full README**: README.md

## 🎯 Keyingi Qadamlar

1. ✅ Loyihani ishga tushiring
2. ✅ Superuser yarating
3. ✅ Admin panel orqali test data kiriting
4. ✅ API endpointlarni test qiling
5. ✅ WebSocket connectionlarni test qiling
6. ✅ QR kod generatsiyasini tekshiring
7. ✅ Buyurtma flow ni test qiling
8. ✅ Real-time notificationlarni tekshiring

Omad! 🚀
