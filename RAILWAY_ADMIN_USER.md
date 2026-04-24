# 👤 Railway Admin User - Yaratish va Boshqarish

## 🔐 Hozirgi Holat

Railway da **hali superuser yaratilmagan**. Shuning uchun admin panelga kirish mumkin emas.

## ✅ Superuser Yaratish (3 ta usul)

### Usul 1: Railway Dashboard (Eng Oson)

1. **Railway dashboard** ga kiring
2. **dastyormenu-backend** service ni tanlang
3. Yuqori o'ng burchakda **⋮** (3 nuqta) → **Shell** ni bosing
4. Terminal ochiladi, quyidagini kiriting:

```bash
python manage.py createsuperuser
```

5. Savollar:
```
Username: admin
Email address: admin@example.com
Password: ********
Password (again): ********
```

6. ✅ Superuser yaratildi!

### Usul 2: Railway CLI

Agar Railway CLI o'rnatilgan bo'lsa:

```bash
# Railway CLI o'rnatish (agar yo'q bo'lsa)
npm install -g @railway/cli

# Login qilish
railway login

# Project ni tanlash
railway link

# Superuser yaratish
railway run python manage.py createsuperuser
```

### Usul 3: Django Management Command (Avtomatik)

Avtomatik superuser yaratish uchun management command yaratamiz:

#### 1. Command faylini yaratish

`apps/users/management/commands/create_admin.py`:

```python
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import os

class Command(BaseCommand):
    help = 'Create admin user if not exists'

    def handle(self, *args, **options):
        username = os.getenv('ADMIN_USERNAME', 'admin')
        email = os.getenv('ADMIN_EMAIL', 'admin@example.com')
        password = os.getenv('ADMIN_PASSWORD', 'admin123')
        
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            self.stdout.write(self.style.SUCCESS(f'Admin user "{username}" created!'))
        else:
            self.stdout.write(self.style.WARNING(f'Admin user "{username}" already exists'))
```

#### 2. Railway Variables ga qo'shish

```bash
ADMIN_USERNAME=admin
ADMIN_EMAIL=admin@dastyormenu.uz
ADMIN_PASSWORD=YourSecurePassword123!
```

#### 3. Start script ga qo'shish

`scripts/start.sh` ga qo'shing:

```bash
echo "Creating admin user..."
python manage.py create_admin
```

## 🔑 Tavsiya Etiladigan Parollar

### Kuchli Parol Yaratish

```bash
# Python bilan
python -c "import secrets, string; print(''.join(secrets.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(20)))"
```

Natija:
```
aB3$xY9#mK2@pL5!qR8%
```

### Parol Talablari

- ✅ Minimum 8 ta belgi
- ✅ Harflar (katta va kichik)
- ✅ Raqamlar
- ✅ Maxsus belgilar (@, #, $, %, !)
- ❌ Oddiy parollar (admin123, password, 12345678)

## 📋 Admin Login Ma'lumotlari

### Local Development

```
URL: http://localhost:8000/admin/
Username: admin
Password: admin123
```

### Railway Production

```
URL: https://dastyormenu-backend-production.up.railway.app/admin/
Username: (siz yaratgan)
Password: (siz yaratgan)
```

## 🔄 Parolni O'zgartirish

### Usul 1: Admin Panel Orqali

1. Admin panelga kiring
2. O'ng yuqori burchakda **Change password** ni bosing
3. Yangi parolni kiriting
4. **Change my password** bosing

### Usul 2: Django Shell

Railway shell da:

```bash
python manage.py shell
```

```python
from django.contrib.auth.models import User

# User ni topish
user = User.objects.get(username='admin')

# Parolni o'zgartirish
user.set_password('YourNewSecurePassword123!')
user.save()

print("Password changed successfully!")
```

### Usul 3: Management Command

```bash
python manage.py changepassword admin
```

Savollar:
```
Password: ********
Password (again): ********
Password changed successfully for user 'admin'
```

## 👥 Qo'shimcha Admin Yaratish

### Railway Shell da

```bash
python manage.py shell
```

```python
from django.contrib.auth.models import User

# Yangi admin yaratish
User.objects.create_superuser(
    username='manager',
    email='manager@dastyormenu.uz',
    password='SecurePassword123!'
)

print("New admin created!")
```

### Yoki createsuperuser

```bash
python manage.py createsuperuser --username manager --email manager@dastyormenu.uz
```

## 🔐 Xavfsizlik Tavsiyalari

### 1. Kuchli Parol Ishlating

❌ **Yomon**:
- admin123
- password
- 12345678
- qwerty

✅ **Yaxshi**:
- aB3$xY9#mK2@pL5!qR8%
- MySecure@Pass2024!
- D@styorMenu#2024

### 2. Parolni Tez-tez O'zgartiring

- Har 3 oyda bir marta
- Agar xavfsizlik buzilsa, darhol

### 3. Parolni Xavfsiz Saqlang

- Password manager ishlating (1Password, LastPass, Bitwarden)
- Hech qachon kodda yoki git da saqlamang
- Environment variables da saqlang

### 4. 2FA (Two-Factor Authentication)

Django admin uchun 2FA qo'shish:

```bash
pip install django-otp qrcode
```

## 📊 Foydalanuvchi Rollari

### Superuser (Admin)

- ✅ Barcha huquqlar
- ✅ Boshqa foydalanuvchilarni boshqarish
- ✅ Barcha ma'lumotlarni ko'rish va o'zgartirish

### Staff User

- ✅ Admin panelga kirish
- ⚠️ Cheklangan huquqlar
- ❌ Foydalanuvchilarni boshqara olmaydi

### Regular User

- ❌ Admin panelga kira olmaydi
- ✅ Faqat API orqali

## 🛠️ Troubleshooting

### 1. "User already exists"

```bash
# Mavjud userni o'chirish
python manage.py shell
```

```python
from django.contrib.auth.models import User
User.objects.filter(username='admin').delete()
```

### 2. Parolni Unutdim

Railway shell da:

```bash
python manage.py changepassword admin
```

### 3. Admin Panel 404

URL to'g'ri ekanligini tekshiring:
```
https://your-app.railway.app/admin/
```

`/admin/` oxirida slash bo'lishi kerak!

### 4. Permission Denied

User superuser ekanligini tekshiring:

```python
from django.contrib.auth.models import User
user = User.objects.get(username='admin')
print(f"Is superuser: {user.is_superuser}")
print(f"Is staff: {user.is_staff}")

# Agar False bo'lsa
user.is_superuser = True
user.is_staff = True
user.save()
```

## 📝 Quick Reference

### Superuser Yaratish
```bash
railway run python manage.py createsuperuser
```

### Parolni O'zgartirish
```bash
railway run python manage.py changepassword admin
```

### Django Shell
```bash
railway run python manage.py shell
```

### Barcha Adminlarni Ko'rish
```python
from django.contrib.auth.models import User
admins = User.objects.filter(is_superuser=True)
for admin in admins:
    print(f"{admin.username} - {admin.email}")
```

## 🎯 Tavsiya Etiladigan Setup

### Railway Production

1. **Superuser yarating**:
   ```bash
   railway run python manage.py createsuperuser
   ```

2. **Kuchli parol ishlating**:
   ```
   Username: admin
   Email: admin@dastyormenu.uz
   Password: (20+ characters, mixed)
   ```

3. **Parolni xavfsiz saqlang**:
   - Password manager
   - Yoki environment variable

4. **Test qiling**:
   ```
   https://your-app.railway.app/admin/
   ```

Omad! 🚀
