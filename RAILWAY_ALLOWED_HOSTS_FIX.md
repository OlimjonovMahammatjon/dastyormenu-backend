# 🔧 Railway ALLOWED_HOSTS Muammosi - YECHIM

## ⚠️ Muammo

```
DisallowedHost: Invalid HTTP_HOST header: 'dastyormenu-backend-production.up.railway.app'. 
You may need to add 'dastyormenu-backend-production.up.railway.app' to ALLOWED_HOSTS.
```

## ✅ YECHIM - Railway Variables

Railway dashboard da **Variables** bo'limiga quyidagini qo'shing:

```bash
ALLOWED_HOSTS=dastyormenu-backend-production.up.railway.app,.railway.app
```

**MUHIM**: 
- Sizning to'liq Railway domain ni kiriting!
- `.railway.app` wildcard qo'shing (barcha Railway subdomain lar uchun)
- Vergul bilan ajrating, bo'sh joy yo'q!

## 📋 TO'LIQ Railway Environment Variables

Railway **Variables** bo'limida quyidagilar bo'lishi kerak:

```bash
# ============================================
# DJANGO CORE (MAJBURIY)
# ============================================
SECRET_KEY=:2KHj@gbyeN3>0SE!QsM-%.O`Hjg!tQ@0vCx7)!etO9se(,*l3
DEBUG=False
DJANGO_SETTINGS_MODULE=config.settings.production

# ============================================
# ALLOWED_HOSTS (MAJBURIY!)
# ============================================
ALLOWED_HOSTS=dastyormenu-backend-production.up.railway.app,.railway.app

# ============================================
# DATABASE (MAJBURIY)
# ============================================
DATABASE_URL=${{Postgres.DATABASE_URL}}

# ============================================
# CSRF (MAJBURIY!)
# ============================================
CSRF_TRUSTED_ORIGINS=https://dastyormenu-backend-production.up.railway.app

# ============================================
# CORS (Frontend uchun - Optional)
# ============================================
CORS_ALLOWED_ORIGINS=https://yourdomain.com

# ============================================
# REDIS (Optional - Celery uchun)
# ============================================
REDIS_URL=${{Redis.REDIS_URL}}
CELERY_BROKER_URL=${{Redis.REDIS_URL}}/0
CELERY_RESULT_BACKEND=${{Redis.REDIS_URL}}/0
```

## 🚀 Qadamlar

### 1. Railway Variables ga Qo'shish

1. Railway dashboard ga kiring
2. Project → **dastyormenu-backend** service
3. **Variables** tab ni oching
4. **+ New Variable** bosing
5. Qo'shing:
   ```
   Name: ALLOWED_HOSTS
   Value: dastyormenu-backend-production.up.railway.app,.railway.app
   ```
6. **Add** bosing

### 2. Redeploy (Avtomatik)

Railway avtomatik ravishda redeploy qiladi. Logs ni kuzating:

```
✅ Starting Dastyor Backend...
✅ Waiting for database...
✅ Database is ready!
✅ Running migrations...
✅ Collecting static files...
✅ Starting server...
✅ Listening on 0.0.0.0:8080
```

### 3. Test Qilish

1. Railway domain ni oching: `https://dastyormenu-backend-production.up.railway.app/`
2. ✅ Swagger UI ko'rinishi kerak
3. Admin panel: `https://dastyormenu-backend-production.up.railway.app/admin/`
4. ✅ Login form ko'rinishi kerak

## 🔍 Railway Domain ni Topish

Agar domain nima ekanligini bilmasangiz:

### Railway Dashboard

1. Project ni oching
2. Service ni tanlang
3. **Settings** → **Networking** → **Domains**
4. Ko'rasiz:
   ```
   dastyormenu-backend-production.up.railway.app
   ```

### Railway CLI

```bash
railway status
```

## 📊 Variables Screenshot

Railway Variables bo'limida ko'rinishi kerak:

```
ALLOWED_HOSTS                 dastyormenu-backend-production.up.railway.app,.railway.app
CSRF_TRUSTED_ORIGINS          https://dastyormenu-backend-production.up.railway.app
DATABASE_URL                  ${{Postgres.DATABASE_URL}}
DEBUG                         False
DJANGO_SETTINGS_MODULE        config.settings.production
SECRET_KEY                    :2KHj@gbyeN3>0SE!QsM-%.O`Hjg!tQ@0vCx7)!etO9se(,*l3
```

## 🐛 Agar Hali Ham Ishlamasa

### 1. Variables Tekshirish

Railway Variables da:
- ✅ `ALLOWED_HOSTS` mavjud
- ✅ To'liq domain kiritilgan
- ✅ `.railway.app` wildcard qo'shilgan
- ✅ Vergul bilan ajratilgan
- ✅ Bo'sh joy yo'q

### 2. Logs Tekshirish

Railway **Deployments** → **View Logs**

Qidiring:
```
ALLOWED_HOSTS = ['dastyormenu-backend-production.up.railway.app', '.railway.app']
```

### 3. Django Shell da Tekshirish

```bash
railway run python manage.py shell
```

```python
from django.conf import settings
print(settings.ALLOWED_HOSTS)
# ['dastyormenu-backend-production.up.railway.app', '.railway.app']
```

### 4. Redeploy Qilish

Railway dashboard da:
1. **Deployments** bo'limiga o'ting
2. Eng so'nggi deployment
3. **⋮** (3 nuqta) → **Redeploy**

## ✅ Muvaffaqiyatli Deploy Belgilari

Logs da ko'rasiz:

```
✅ Starting Dastyor Backend...
✅ Waiting for database...
✅ Database is ready!
✅ Running migrations...
✅ Operations to perform:
✅   Apply all migrations: ...
✅ Running migrations:
✅   Applying contenttypes.0001_initial... OK
✅   ... (barcha migrations)
✅ Collecting static files...
✅ 150 static files copied
✅ Starting server...
✅ Listening on 0.0.0.0:8080
```

Va xatolik yo'q:
- ❌ `DisallowedHost` yo'q
- ❌ `Invalid HTTP_HOST` yo'q
- ❌ `Bad Request (400)` yo'q

## 🎯 Natija

Agar barcha to'g'ri bo'lsa:

1. ✅ Swagger UI: `https://dastyormenu-backend-production.up.railway.app/`
2. ✅ Admin Panel: `https://dastyormenu-backend-production.up.railway.app/admin/`
3. ✅ API: `https://dastyormenu-backend-production.up.railway.app/api/`
4. ✅ Xatolik yo'q!

## 📝 Minimal Railway Variables (Faqat Kerakli)

Agar minimal sozlash kerak bo'lsa:

```bash
# Faqat bu 5 ta variable kerak!
SECRET_KEY=:2KHj@gbyeN3>0SE!QsM-%.O`Hjg!tQ@0vCx7)!etO9se(,*l3
DEBUG=False
DJANGO_SETTINGS_MODULE=config.settings.production
DATABASE_URL=${{Postgres.DATABASE_URL}}
ALLOWED_HOSTS=dastyormenu-backend-production.up.railway.app,.railway.app
CSRF_TRUSTED_ORIGINS=https://dastyormenu-backend-production.up.railway.app
```

## 🔐 Security Checklist

- [x] `SECRET_KEY` o'zgartirildi
- [x] `DEBUG=False`
- [x] `ALLOWED_HOSTS` to'g'ri sozlandi
- [x] `CSRF_TRUSTED_ORIGINS` to'g'ri sozlandi
- [x] `DATABASE_URL` reference qilindi
- [x] HTTPS avtomatik (Railway)

## 📞 Qo'shimcha Yordam

Agar hali ham muammo bo'lsa:

1. **Railway Variables ni screenshot qiling**
2. **Logs ni to'liq ko'ring**
3. **Browser cache ni tozalang**
4. **Incognito mode da sinab ko'ring**

Railway Discord: https://discord.gg/railway

Omad! 🚀
