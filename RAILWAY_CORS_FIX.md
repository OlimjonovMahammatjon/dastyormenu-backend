# 🔧 Railway CORS Muammosini Hal Qilish

## ❌ Muammo

Frontend dan Railway backend ga so'rov yuborilganda CORS xatosi:

```
Access to fetch at 'https://dastyormenu-backend-production.up.railway.app/api/auth/login' 
from origin 'http://localhost:5174' has been blocked by CORS policy: 
Response to preflight request doesn't pass access control check: 
No 'Access-Control-Allow-Origin' header is present on the requested resource.
```

## ✅ Yechim

### Variant 1: Barcha Originlarni Ruxsat Etish (Test uchun)

Railway **Variables** da:

```bash
# CORS_ALLOWED_ORIGINS ni qo'shmasangiz, avtomatik barcha originlar ruxsat etiladi
# Faqat test uchun! Production da aniq originlarni kiriting!
```

Bu holda `CORS_ALLOW_ALL_ORIGINS = True` bo'ladi.

---

### Variant 2: Aniq Originlarni Belgilash (Production uchun - TAVSIYA ETILADI)

Railway **Variables** → **+ New Variable**:

```bash
CORS_ALLOWED_ORIGINS=http://localhost:5174,http://localhost:3000,https://yourdomain.com
```

**MUHIM**: 
- Vergul bilan ajrating, bo'sh joy yo'q!
- `http://` yoki `https://` bilan boshlang!
- Port raqamini kiriting (masalan: `:5174`)

---

## 📋 To'liq Railway Variables

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
# CORS (TAVSIYA ETILADI)
# ============================================
CORS_ALLOWED_ORIGINS=http://localhost:5174,http://localhost:3000,https://yourdomain.com

# ============================================
# ADMIN USER (OPTIONAL)
# ============================================
ADMIN_USERNAME=admin
ADMIN_EMAIL=admin@dastyormenu.uz
ADMIN_PASSWORD=admin123
```

---

## 🔍 CORS Sozlamalari

### Hozirgi Kod (production.py)

```python
# CORS Settings
cors_origins = os.getenv('CORS_ALLOWED_ORIGINS', '').split(',')
if cors_origins and cors_origins[0]:
    CORS_ALLOWED_ORIGINS = [origin.strip() for origin in cors_origins]
else:
    # Default: Allow all origins
    CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]
```

---

## 🚀 Deploy Qilish

### 1. Git Push

```bash
git add .
git commit -m "Fixed CORS for Railway production"
git push origin main
```

### 2. Railway Variables Qo'shish

Railway dashboard → **Variables** → **+ New Variable**:

**Test uchun** (barcha originlar):
```bash
# CORS_ALLOWED_ORIGINS ni qo'shmang, avtomatik CORS_ALLOW_ALL_ORIGINS=True bo'ladi
```

**Production uchun** (aniq originlar):
```bash
CORS_ALLOWED_ORIGINS=http://localhost:5174,https://yourdomain.com
```

### 3. Redeploy

Railway avtomatik redeploy qiladi yoki:
- Railway dashboard → **Deployments** → **Redeploy**

---

## 🧪 Test Qilish

### 1. Browser Console

Frontend da (http://localhost:5174):

```javascript
fetch('https://dastyormenu-backend-production.up.railway.app/api/auth/login/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    login: 'admin',
    password: 'admin123'
  })
})
.then(res => res.json())
.then(data => console.log('✅ Success:', data))
.catch(err => console.error('❌ Error:', err));
```

### 2. cURL Test

```bash
curl -X POST https://dastyormenu-backend-production.up.railway.app/api/auth/login/ \
  -H "Content-Type: application/json" \
  -H "Origin: http://localhost:5174" \
  -d '{"login":"admin","password":"admin123"}'
```

Javobda `Access-Control-Allow-Origin` header bo'lishi kerak:

```
Access-Control-Allow-Origin: http://localhost:5174
```

---

## 🐛 Troubleshooting

### 1. Hali Ham CORS Xatosi

**Tekshiring**:
1. Railway Variables da `CORS_ALLOWED_ORIGINS` to'g'ri yozilganini
2. Vergul bilan ajratilganini (bo'sh joy yo'q!)
3. `http://` yoki `https://` bilan boshlanganini
4. Port raqami to'g'ri yozilganini

**Misol**:
```bash
# ✅ To'g'ri
CORS_ALLOWED_ORIGINS=http://localhost:5174,https://app.example.com

# ❌ Noto'g'ri (bo'sh joy bor)
CORS_ALLOWED_ORIGINS=http://localhost:5174, https://app.example.com

# ❌ Noto'g'ri (http:// yo'q)
CORS_ALLOWED_ORIGINS=localhost:5174

# ❌ Noto'g'ri (port yo'q)
CORS_ALLOWED_ORIGINS=http://localhost
```

### 2. Preflight Request Failed

**Xato**:
```
Response to preflight request doesn't pass access control check
```

**Yechim**:
1. `CORS_ALLOW_METHODS` da `OPTIONS` borligini tekshiring
2. `CORS_ALLOW_HEADERS` da kerakli headerlar borligini tekshiring
3. Railway logs ni tekshiring

### 3. Credentials Not Allowed

**Xato**:
```
The value of the 'Access-Control-Allow-Credentials' header in the response is '' 
which must be 'true' when the request's credentials mode is 'include'.
```

**Yechim**:
```python
CORS_ALLOW_CREDENTIALS = True
```

Bu allaqachon sozlangan!

### 4. Railway Logs Tekshirish

Railway dashboard → **Deployments** → **View logs**

Qidiring:
```
CORS_ALLOW_ALL_ORIGINS = True
```

yoki

```
CORS_ALLOWED_ORIGINS = ['http://localhost:5174', ...]
```

---

## 📊 CORS Sozlamalari Jadvali

| Sozlama | Qiymat | Tavsif |
|---------|--------|--------|
| `CORS_ALLOW_ALL_ORIGINS` | `True` | Barcha originlarni ruxsat etish (test uchun) |
| `CORS_ALLOWED_ORIGINS` | `['http://localhost:5174']` | Aniq originlar ro'yxati (production uchun) |
| `CORS_ALLOW_CREDENTIALS` | `True` | Cookie va auth headerlarni ruxsat etish |
| `CORS_ALLOW_METHODS` | `['GET', 'POST', ...]` | Ruxsat etilgan HTTP metodlar |
| `CORS_ALLOW_HEADERS` | `['authorization', ...]` | Ruxsat etilgan headerlar |

---

## 🔐 Xavfsizlik

### Test Muhitida

```bash
# Barcha originlarni ruxsat etish
# CORS_ALLOWED_ORIGINS ni qo'shmang
```

### Production Muhitida

```bash
# Faqat aniq originlarni ruxsat etish
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://app.yourdomain.com
```

**MUHIM**: Production da `CORS_ALLOW_ALL_ORIGINS = True` ishlatmang!

---

## ✅ Checklist

Deploy qilishdan oldin:

- [ ] `config/settings/production.py` da CORS sozlamalari to'g'ri
- [ ] Railway Variables da `CORS_ALLOWED_ORIGINS` qo'shildi (yoki qo'shilmadi - barcha originlar uchun)
- [ ] Git push qilindi
- [ ] Railway redeploy qilindi
- [ ] Logs tekshirildi
- [ ] Frontend dan test qilindi
- [ ] Browser console da CORS xatosi yo'q

---

## 🎉 Natija

Agar barcha qadamlar to'g'ri bajarilgan bo'lsa:

✅ Frontend (http://localhost:5174) → Backend (Railway) so'rovlar ishlaydi
✅ CORS xatosi yo'q
✅ Login, API so'rovlar ishlaydi

---

## 📞 Keyingi Qadamlar

### 1. Production Domain Qo'shish

Agar production domain bo'lsa:

```bash
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://app.yourdomain.com
```

### 2. Multiple Environments

Development, Staging, Production uchun:

```bash
CORS_ALLOWED_ORIGINS=http://localhost:5174,https://staging.yourdomain.com,https://yourdomain.com
```

### 3. Wildcard Subdomain (Ehtiyotkorlik bilan!)

```python
# production.py da
CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^https://\w+\.yourdomain\.com$",
]
```

Omad! 🚀
