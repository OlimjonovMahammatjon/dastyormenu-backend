# 🚀 Railway Deploy - To'liq Qo'llanma

## ❌ Muammo: ALLOWED_HOSTS Xatosi

```
DisallowedHost: Invalid HTTP_HOST header: 'dastyormenu-backend-production.up.railway.app'
```

Bu xato Railway da `ALLOWED_HOSTS` environment variable to'g'ri sozlanmaganligini bildiradi.

## ✅ Yechim: To'liq Sozlash

### 1️⃣ SECRET_KEY Yaratish

```bash
python scripts/generate_secret_key.py
```

Natija (misol):
```
SECRET_KEY=:2KHj@gbyeN3>0SE!QsM-%.O`Hjg!tQ@0vCx7)!etO9se(,*l3
```

**MUHIM**: Bu sizning SECRET_KEY ingiz! Nusxa oling!

---

### 2️⃣ Railway Environment Variables

Railway dashboard → **Variables** → **+ New Variable**

Quyidagi **BARCHA** o'zgaruvchilarni qo'shing:

```bash
# ============================================
# 1. DJANGO CORE (MAJBURIY!)
# ============================================
SECRET_KEY=:2KHj@gbyeN3>0SE!QsM-%.O`Hjg!tQ@0vCx7)!etO9se(,*l3
DEBUG=False
DJANGO_SETTINGS_MODULE=config.settings.production

# ============================================
# 2. ALLOWED_HOSTS (MAJBURIY!)
# ============================================
ALLOWED_HOSTS=dastyormenu-backend-production.up.railway.app,.railway.app

# ============================================
# 3. CSRF TRUSTED ORIGINS (MAJBURIY!)
# ============================================
CSRF_TRUSTED_ORIGINS=https://dastyormenu-backend-production.up.railway.app

# ============================================
# 4. DATABASE (MAJBURIY!)
# ============================================
DATABASE_URL=${{Postgres.DATABASE_URL}}

# ============================================
# 5. ADMIN USER (TAVSIYA ETILADI)
# ============================================
ADMIN_USERNAME=admin
ADMIN_EMAIL=admin@dastyormenu.uz
ADMIN_PASSWORD=YourSecurePassword123!
```

---

### 3️⃣ Railway Domain Nomini Topish

Agar sizning Railway domain nomingiz boshqa bo'lsa:

1. Railway dashboard → **Settings** → **Domains**
2. Domain nomini ko'ring (masalan: `your-app-name.up.railway.app`)
3. `ALLOWED_HOSTS` va `CSRF_TRUSTED_ORIGINS` da o'zgartiring

**Misol**:
```bash
# Agar sizning domain: myapp.up.railway.app
ALLOWED_HOSTS=myapp.up.railway.app,.railway.app
CSRF_TRUSTED_ORIGINS=https://myapp.up.railway.app
```

---

### 4️⃣ PostgreSQL Service Qo'shish

Agar hali qo'shilmagan bo'lsa:

1. Railway dashboard → **+ New** → **Database** → **PostgreSQL**
2. Avtomatik `DATABASE_URL` yaratiladi
3. Variables da `DATABASE_URL=${{Postgres.DATABASE_URL}}` qo'shing

---

### 5️⃣ Deploy Qilish

```bash
# Barcha o'zgarishlarni commit qiling
git add .
git commit -m "Fixed ALLOWED_HOSTS for Railway"
git push origin main
```

Railway avtomatik deploy qiladi!

---

## 📋 To'liq Variables Ro'yxati

Railway **Variables** da quyidagilar bo'lishi kerak:

| Variable | Qiymat | Majburiy? |
|----------|--------|-----------|
| `SECRET_KEY` | `generate_secret_key.py` dan | ✅ Ha |
| `DEBUG` | `False` | ✅ Ha |
| `DJANGO_SETTINGS_MODULE` | `config.settings.production` | ✅ Ha |
| `ALLOWED_HOSTS` | `your-app.up.railway.app,.railway.app` | ✅ Ha |
| `CSRF_TRUSTED_ORIGINS` | `https://your-app.up.railway.app` | ✅ Ha |
| `DATABASE_URL` | `${{Postgres.DATABASE_URL}}` | ✅ Ha |
| `ADMIN_USERNAME` | `admin` | ⚠️ Tavsiya |
| `ADMIN_EMAIL` | `admin@example.com` | ⚠️ Tavsiya |
| `ADMIN_PASSWORD` | `admin123` | ⚠️ Tavsiya |

---

## 🔍 Deploy Logs Tekshirish

Railway dashboard → **Deployments** → **View logs**

### ✅ Muvaffaqiyatli Deploy

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
✅ Listening on TCP address 0.0.0.0:8080
```

### ❌ ALLOWED_HOSTS Xatosi

```
❌ DisallowedHost: Invalid HTTP_HOST header
```

**Yechim**: `ALLOWED_HOSTS` variable ni tekshiring!

---

## 🌐 Test Qilish

### 1. Swagger UI

```
https://dastyormenu-backend-production.up.railway.app/
```

Ko'rinishi kerak:
- ✅ Swagger UI sahifasi
- ✅ Barcha API endpoints
- ✅ "Try it out" tugmalari

### 2. Admin Panel

```
https://dastyormenu-backend-production.up.railway.app/admin/
```

Login:
- **Username**: `admin` (yoki sizning `ADMIN_USERNAME`)
- **Password**: `admin123` (yoki sizning `ADMIN_PASSWORD`)

Ko'rinishi kerak:
- ✅ Django admin login sahifasi
- ✅ Login qilish ishlaydi
- ✅ Admin dashboard

### 3. API Test

Swagger UI da:
1. **POST /api/auth/login/** ni oching
2. **Try it out** bosing
3. Ma'lumot kiriting:
```json
{
  "login": "admin",
  "password": "admin123"
}
```
4. **Execute** bosing

Natija:
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "username": "admin",
    "email": "admin@example.com"
  }
}
```

---

## 🐛 Troubleshooting

### 1. ALLOWED_HOSTS Xatosi

**Xato**:
```
DisallowedHost: Invalid HTTP_HOST header
```

**Yechim**:
1. Railway Variables da `ALLOWED_HOSTS` borligini tekshiring
2. Domain nomini to'g'ri yozganingizni tekshiring
3. Vergul bilan ajratilganini tekshiring: `domain1.com,domain2.com`
4. Redeploy qiling

### 2. CSRF Xatosi

**Xato**:
```
CSRF verification failed
```

**Yechim**:
1. `CSRF_TRUSTED_ORIGINS` borligini tekshiring
2. `https://` bilan boshlanishini tekshiring
3. Domain nomini to'g'ri yozganingizni tekshiring
4. Redeploy qiling

### 3. Database Connection Xatosi

**Xato**:
```
could not connect to server
```

**Yechim**:
1. PostgreSQL service qo'shilganini tekshiring
2. `DATABASE_URL=${{Postgres.DATABASE_URL}}` to'g'ri yozilganini tekshiring
3. Redeploy qiling

### 4. Admin User Yaratilmadi

**Xato**:
```
No such user
```

**Yechim**:
1. Logs da "Creating admin user..." ni qidiring
2. Agar xato bo'lsa, `ADMIN_USERNAME`, `ADMIN_EMAIL`, `ADMIN_PASSWORD` tekshiring
3. Railway CLI bilan manual yaratish:

```bash
railway run python manage.py createsuperuser
```

### 5. Static Files 404

**Xato**:
```
GET /static/admin/css/base.css 404
```

**Yechim**:
1. Logs da "Collecting static files..." ni qidiring
2. WhiteNoise o'rnatilganini tekshiring: `pip list | grep whitenoise`
3. Redeploy qiling

---

## 📊 Railway Services Arxitekturasi

```
┌─────────────────────────────────────────────┐
│  Django Service (Daphne)                    │
│  ├─ Swagger UI: /                           │
│  ├─ Admin Panel: /admin/                    │
│  ├─ API: /api/                              │
│  └─ Static Files: /static/ (WhiteNoise)     │
└─────────────────────────────────────────────┘
                    │
                    │ DATABASE_URL
                    ▼
┌─────────────────────────────────────────────┐
│  PostgreSQL Service                         │
│  ├─ Auto-generated DATABASE_URL             │
│  ├─ Auto backups                            │
│  └─ Persistent storage                      │
└─────────────────────────────────────────────┘
```

---

## ✅ Final Checklist

Deploy qilishdan oldin tekshiring:

- [ ] `SECRET_KEY` yaratildi va nusxa olindi
- [ ] Railway project yaratildi
- [ ] PostgreSQL service qo'shildi
- [ ] **BARCHA** environment variables qo'shildi:
  - [ ] `SECRET_KEY`
  - [ ] `DEBUG=False`
  - [ ] `DJANGO_SETTINGS_MODULE=config.settings.production`
  - [ ] `ALLOWED_HOSTS` (to'g'ri domain bilan!)
  - [ ] `CSRF_TRUSTED_ORIGINS` (https:// bilan!)
  - [ ] `DATABASE_URL=${{Postgres.DATABASE_URL}}`
  - [ ] `ADMIN_USERNAME` (optional)
  - [ ] `ADMIN_EMAIL` (optional)
  - [ ] `ADMIN_PASSWORD` (optional)
- [ ] Git push qilindi
- [ ] Railway deploy qilindi
- [ ] Logs tekshirildi (xatolar yo'q)
- [ ] Swagger UI ochildi
- [ ] Admin panelga kirish test qilindi
- [ ] API login test qilindi

---

## 🎉 Muvaffaqiyatli Deploy!

Agar barcha qadamlar to'g'ri bajarilgan bo'lsa:

✅ **Swagger UI**: https://your-app.up.railway.app/
✅ **Admin Panel**: https://your-app.up.railway.app/admin/
✅ **API**: https://your-app.up.railway.app/api/

**Admin Login**:
- Username: `admin`
- Password: `admin123` (yoki sizning paroli)

⚠️ **Xavfsizlik**: Birinchi login qilgandan keyin admin parolni o'zgartiring!

---

## 📞 Keyingi Qadamlar

1. **Custom Domain Qo'shish** (optional):
   - Railway → Settings → Domains → Add Domain
   - DNS sozlash
   - `ALLOWED_HOSTS` va `CSRF_TRUSTED_ORIGINS` yangilash

2. **Redis Qo'shish** (optional, Celery uchun):
   - Railway → + New → Database → Redis
   - `REDIS_URL=${{Redis.REDIS_URL}}` qo'shish

3. **S3 Storage** (optional, rasm yuklash uchun):
   - AWS S3 bucket yaratish
   - Environment variables qo'shish:
     - `USE_S3=True`
     - `AWS_ACCESS_KEY_ID`
     - `AWS_SECRET_ACCESS_KEY`
     - `AWS_STORAGE_BUCKET_NAME`

4. **Monitoring** (optional):
   - Railway → Metrics
   - CPU, Memory, Network monitoring

Omad! 🚀
