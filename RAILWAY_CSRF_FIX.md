# 🔧 Railway CSRF Muammosini Hal Qilish

## ⚠️ Muammo

Admin panelga kirishda:
```
CSRF tekshiruvi amalga oshmadi. So'rov bekor qilindi.
Origin checking failed - https://dastyormenu-backend-production.up.railway.app does not match any trusted origins.
```

## ✅ Yechim

### Railway Variables da Qo'shish Kerak

Railway dashboard da **Variables** bo'limiga o'ting va quyidagini qo'shing:

```bash
CSRF_TRUSTED_ORIGINS=https://dastyormenu-backend-production.up.railway.app
```

**MUHIM**: Sizning to'liq Railway domain ni kiriting!

### Agar Bir Nechta Domain Bo'lsa

```bash
CSRF_TRUSTED_ORIGINS=https://dastyormenu-backend-production.up.railway.app,https://yourdomain.com
```

Vergul bilan ajrating, bo'sh joy yo'q!

## 📋 To'liq Railway Environment Variables

```bash
# ============================================
# DJANGO CORE (MAJBURIY)
# ============================================
SECRET_KEY=:2KHj@gbyeN3>0SE!QsM-%.O`Hjg!tQ@0vCx7)!etO9se(,*l3
DEBUG=False
DJANGO_SETTINGS_MODULE=config.settings.production

# ============================================
# DATABASE (MAJBURIY)
# ============================================
DATABASE_URL=${{Postgres.DATABASE_URL}}

# ============================================
# CSRF (MAJBURIY - Sizning domain)
# ============================================
CSRF_TRUSTED_ORIGINS=https://dastyormenu-backend-production.up.railway.app

# ============================================
# ALLOWED_HOSTS (Optional)
# ============================================
ALLOWED_HOSTS=dastyormenu-backend-production.up.railway.app,.railway.app

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

## 🔍 Railway Domain ni Topish

### 1. Railway Dashboard

1. Project ni oching
2. Django service ni tanlang
3. **Settings** → **Networking**
4. **Domains** bo'limida ko'rasiz:
   ```
   dastyormenu-backend-production.up.railway.app
   ```

### 2. Railway CLI

```bash
railway status
```

Natija:
```
Service: dastyormenu-backend-production
Domain: https://dastyormenu-backend-production.up.railway.app
```

## 🚀 Deploy Qilish

### 1. Git Push

```bash
git add .
git commit -m "Fixed CSRF for Railway"
git push origin main
```

### 2. Railway Variables Qo'shish

1. Railway dashboard ga kiring
2. Project → Django service
3. **Variables** bo'limiga o'ting
4. **+ New Variable** bosing
5. Qo'shing:
   ```
   CSRF_TRUSTED_ORIGINS=https://dastyormenu-backend-production.up.railway.app
   ```
6. **Add** bosing

### 3. Redeploy (Avtomatik)

Railway avtomatik ravishda redeploy qiladi.

### 4. Test Qilish

1. Railway domain ni oching: `https://dastyormenu-backend-production.up.railway.app/admin/`
2. Login qiling
3. ✅ CSRF xatolik yo'q!

## 🐛 Agar Hali Ham Ishlamasa

### 1. Variables Tekshirish

Railway dashboard da **Variables** bo'limini oching va tekshiring:

```bash
CSRF_TRUSTED_ORIGINS=https://dastyormenu-backend-production.up.railway.app
```

- ✅ `https://` bor
- ✅ To'liq domain
- ✅ Bo'sh joy yo'q
- ✅ Vergul yo'q (bitta domain bo'lsa)

### 2. Redeploy Qilish

Railway dashboard da:
1. **Deployments** bo'limiga o'ting
2. Eng so'nggi deployment ni tanlang
3. **⋮** (3 nuqta) → **Redeploy**

### 3. Logs Tekshirish

Railway dashboard da **Deployments** → **View Logs**

Quyidagini qidiring:
```
CSRF_TRUSTED_ORIGINS = ['https://dastyormenu-backend-production.up.railway.app']
```

### 4. Django Shell da Tekshirish

Railway shell da:

```bash
railway run python manage.py shell
```

```python
from django.conf import settings
print(settings.CSRF_TRUSTED_ORIGINS)
# ['https://dastyormenu-backend-production.up.railway.app']
```

## 📝 Production Settings

`config/settings/production.py` da:

```python
# CSRF Settings
csrf_origins = os.getenv('CSRF_TRUSTED_ORIGINS', '').split(',')
if csrf_origins and csrf_origins[0]:
    CSRF_TRUSTED_ORIGINS = [origin.strip() for origin in csrf_origins if origin.strip()]
else:
    CSRF_TRUSTED_ORIGINS = []

# Security - Railway uchun
SECURE_SSL_REDIRECT = False  # Railway o'zi HTTPS ni boshqaradi
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
CSRF_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_SAMESITE = 'Lax'
X_FRAME_OPTIONS = 'SAMEORIGIN'
```

## ✅ Checklist

- [ ] `CSRF_TRUSTED_ORIGINS` variable qo'shildi
- [ ] To'liq Railway domain kiritildi
- [ ] `https://` bilan boshlandi
- [ ] Bo'sh joy yo'q
- [ ] Redeploy qilindi
- [ ] Logs tekshirildi
- [ ] Admin panelga kirish test qilindi

## 🎯 Natija

Agar barcha qadamlar to'g'ri bajarilsa:

1. ✅ Admin panel ochiladi
2. ✅ Login form ko'rinadi
3. ✅ Login qilish mumkin
4. ✅ CSRF xatolik yo'q

## 📞 Qo'shimcha Yordam

Agar hali ham ishlamasa:

1. **Railway domain ni to'g'ri nusxalang**:
   - Railway dashboard dan copy qiling
   - Qo'lda yozishga urinmang

2. **Browser cache ni tozalang**:
   - Ctrl+Shift+Delete
   - Cookies va cache ni tozalang

3. **Incognito mode da sinab ko'ring**:
   - Yangi incognito window oching
   - Admin panelga kiring

4. **Railway support**:
   - Railway Discord: https://discord.gg/railway
   - Railway Docs: https://docs.railway.app

Omad! 🚀
