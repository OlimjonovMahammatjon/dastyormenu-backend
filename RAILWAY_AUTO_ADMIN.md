# 🤖 Railway Avtomatik Admin Yaratish

## ✅ Yangi Funksiya

Endi Railway deploy qilganda **avtomatik ravishda admin user yaratiladi**!

## 🔧 Qanday Ishlaydi

### 1. Management Command

`apps/users/management/commands/create_admin.py` yaratildi:
- Har safar deploy qilganda ishga tushadi
- Agar admin mavjud bo'lmasa, yaratadi
- Agar mavjud bo'lsa, o'tkazib yuboradi

### 2. Start Script

`scripts/start.sh` ga qo'shildi:
```bash
echo "Creating admin user..."
python manage.py create_admin
```

## 🔑 Default Admin Ma'lumotlari

Agar Railway Variables da sozlanmagan bo'lsa:

```
Username: admin
Email: admin@example.com
Password: admin123
```

⚠️ **MUHIM**: Bu default parol xavfsiz emas! O'zgartiring!

## 🎯 Admin Ma'lumotlarini Sozlash

### Railway Variables ga Qo'shing

Railway dashboard → **Variables** → **+ New Variable**:

```bash
# Admin User Settings
ADMIN_USERNAME=admin
ADMIN_EMAIL=admin@dastyormenu.uz
ADMIN_PASSWORD=YourSecurePassword123!
```

### Tavsiya Etiladigan Sozlash

```bash
ADMIN_USERNAME=dastyormenu_admin
ADMIN_EMAIL=admin@dastyormenu.uz
ADMIN_PASSWORD=aB3$xY9#mK2@pL5!qR8%
```

## 🚀 Deploy Qilish

### 1. Git Push

```bash
git add .
git commit -m "Added auto admin creation"
git push origin main
```

### 2. Railway Avtomatik Deploy

Railway logs da ko'rasiz:

```
✅ Starting Dastyor Backend...
✅ Waiting for database...
✅ Database is ready!
✅ Running migrations...
✅ Creating admin user...
✅ Admin user "admin" created successfully!
📧 Email: admin@example.com
🔑 Password: admin123
✅ Collecting static files...
✅ Starting server...
```

### 3. Admin Panelga Kirish

```
URL: https://dastyormenu-backend-production.up.railway.app/admin/
Username: admin (yoki sizning ADMIN_USERNAME)
Password: admin123 (yoki sizning ADMIN_PASSWORD)
```

## 🔄 Parolni O'zgartirish

### Usul 1: Railway Variables Orqali

1. Railway Variables da `ADMIN_PASSWORD` ni o'zgartiring
2. Admin userni o'chiring (Django shell orqali)
3. Redeploy qiling - yangi parol bilan yaratiladi

### Usul 2: Admin Panel Orqali

1. Admin panelga kiring
2. O'ng yuqori burchakda **Change password**
3. Yangi parolni kiriting
4. Saqlang

### Usul 3: Railway CLI

```bash
# Railway CLI o'rnatish
npm install -g @railway/cli

# Login
railway login

# Project link
railway link

# Django shell
railway run python manage.py shell
```

```python
from django.contrib.auth.models import User
user = User.objects.get(username='admin')
user.set_password('YourNewPassword123!')
user.save()
```

## 📋 Railway Variables (To'liq)

```bash
# ============================================
# DJANGO CORE (MAJBURIY)
# ============================================
SECRET_KEY=:2KHj@gbyeN3>0SE!QsM-%.O`Hjg!tQ@0vCx7)!etO9se(,*l3
DEBUG=False
DJANGO_SETTINGS_MODULE=config.settings.production

# ============================================
# ALLOWED_HOSTS & CSRF (MAJBURIY)
# ============================================
ALLOWED_HOSTS=dastyormenu-backend-production.up.railway.app,.railway.app
CSRF_TRUSTED_ORIGINS=https://dastyormenu-backend-production.up.railway.app

# ============================================
# DATABASE (MAJBURIY)
# ============================================
DATABASE_URL=${{Postgres.DATABASE_URL}}

# ============================================
# ADMIN USER (TAVSIYA ETILADI)
# ============================================
ADMIN_USERNAME=dastyormenu_admin
ADMIN_EMAIL=admin@dastyormenu.uz
ADMIN_PASSWORD=YourSecurePassword123!

# ============================================
# CORS (Optional - Frontend uchun)
# ============================================
CORS_ALLOWED_ORIGINS=https://yourdomain.com

# ============================================
# REDIS (Optional - Celery uchun)
# ============================================
REDIS_URL=${{Redis.REDIS_URL}}
CELERY_BROKER_URL=${{Redis.REDIS_URL}}/0
CELERY_RESULT_BACKEND=${{Redis.REDIS_URL}}/0
```

## 🔐 Xavfsizlik

### Kuchli Parol Yaratish

```bash
# Python bilan
python -c "import secrets, string; print(''.join(secrets.choice(string.ascii_letters + string.digits + '!@#$%^&*') for _ in range(24)))"
```

Natija:
```
aB3$xY9#mK2@pL5!qR8%tU6^
```

### Parol Talablari

- ✅ Minimum 12 ta belgi
- ✅ Katta harflar (A-Z)
- ✅ Kichik harflar (a-z)
- ✅ Raqamlar (0-9)
- ✅ Maxsus belgilar (!@#$%^&*)
- ❌ Oddiy parollar (admin123, password)

## 🐛 Troubleshooting

### 1. Admin User Yaratilmadi

Logs ni tekshiring:
```
Railway dashboard → Deployments → View logs
```

Qidiring:
```
Creating admin user...
Admin user "admin" created successfully!
```

### 2. "Admin already exists"

Bu normal! Agar admin mavjud bo'lsa, qayta yaratmaydi.

Agar parolni unutgan bo'lsangiz:
1. Railway Variables da `ADMIN_PASSWORD` ni o'zgartiring
2. Railway CLI bilan admin userni o'chiring:
```bash
railway run python manage.py shell
```
```python
from django.contrib.auth.models import User
User.objects.filter(username='admin').delete()
```
3. Redeploy qiling

### 3. Login Qila Olmayapman

Tekshiring:
- ✅ Username to'g'ri (default: `admin`)
- ✅ Password to'g'ri (default: `admin123`)
- ✅ ALLOWED_HOSTS sozlangan
- ✅ CSRF_TRUSTED_ORIGINS sozlangan

## ✅ Checklist

Deploy qilishdan oldin:

- [ ] `apps/users/management/commands/create_admin.py` yaratildi
- [ ] `scripts/start.sh` yangilandi
- [ ] Railway Variables da `ADMIN_USERNAME` sozlandi (optional)
- [ ] Railway Variables da `ADMIN_EMAIL` sozlandi (optional)
- [ ] Railway Variables da `ADMIN_PASSWORD` sozlandi (optional)
- [ ] Git push qilindi
- [ ] Railway deploy qilindi
- [ ] Logs tekshirildi
- [ ] Admin panelga kirish test qilindi

## 🎉 Natija

Endi har safar Railway ga deploy qilganda:

1. ✅ Database tayyor bo'lishini kutadi
2. ✅ Migrations bajaradi
3. ✅ **Admin user avtomatik yaratadi**
4. ✅ Static files yig'adi
5. ✅ Server ishga tushadi

Admin panelga kirish:
```
https://dastyormenu-backend-production.up.railway.app/admin/
Username: admin (yoki sizning)
Password: admin123 (yoki sizning)
```

⚠️ **Eslatma**: Birinchi deploy qilgandan keyin parolni o'zgartiring!

Omad! 🚀
