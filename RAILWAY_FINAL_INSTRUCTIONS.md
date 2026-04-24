# 🎯 Railway Deploy - Yakuniy Ko'rsatmalar

## 📝 Nima Qilindi?

### ✅ Kod O'zgarishlari

1. **production.py** yangilandi:
   - `ALLOWED_HOSTS` environment variable dan o'qiladi
   - Agar bo'sh bo'lsa, default `['*']` (faqat test uchun)
   - `CSRF_TRUSTED_ORIGINS` avtomatik `ALLOWED_HOSTS` dan yaratiladi

2. **Admin User Auto-Creation**:
   - Har deploy qilganda avtomatik admin yaratiladi
   - Default: `admin` / `admin123`
   - Environment variables orqali sozlanadi

3. **Swagger UI**:
   - Root URL da: `/`
   - Admin panel: `/admin/`

---

## 🚀 Railway ga Deploy Qilish

### Qadam 1: SECRET_KEY Yaratish

```bash
python scripts/generate_secret_key.py
```

**Natijani saqlang!** Masalan:
```
SECRET_KEY=:2KHj@gbyeN3>0SE!QsM-%.O`Hjg!tQ@0vCx7)!etO9se(,*l3
```

---

### Qadam 2: Railway Project Yaratish

1. https://railway.app ga kiring
2. **New Project** → **Deploy from GitHub repo**
3. Repository ni tanlang (masalan: `dastyor-backend`)

---

### Qadam 3: PostgreSQL Qo'shish

1. Railway project ichida → **+ New**
2. **Database** → **PostgreSQL**
3. Avtomatik `DATABASE_URL` yaratiladi

---

### Qadam 4: Environment Variables Qo'shish

Railway dashboard → **Variables** → **+ New Variable**

**DIQQAT**: Sizning Railway domain nomingizni yozing!

Domain nomini topish:
- Railway → **Settings** → **Domains**
- Masalan: `dastyormenu-backend-production.up.railway.app`

**Quyidagi BARCHA o'zgaruvchilarni qo'shing**:

```bash
# 1. Django Core (MAJBURIY)
SECRET_KEY=:2KHj@gbyeN3>0SE!QsM-%.O`Hjg!tQ@0vCx7)!etO9se(,*l3
DEBUG=False
DJANGO_SETTINGS_MODULE=config.settings.production

# 2. Allowed Hosts (MAJBURIY - sizning domain nomingiz!)
ALLOWED_HOSTS=dastyormenu-backend-production.up.railway.app,.railway.app

# 3. CSRF (MAJBURIY - https:// bilan!)
CSRF_TRUSTED_ORIGINS=https://dastyormenu-backend-production.up.railway.app

# 4. Database (MAJBURIY)
DATABASE_URL=${{Postgres.DATABASE_URL}}

# 5. Admin User (TAVSIYA ETILADI)
ADMIN_USERNAME=admin
ADMIN_EMAIL=admin@dastyormenu.uz
ADMIN_PASSWORD=YourSecurePassword123!
```

**MUHIM Qoidalar**:
- ✅ `ALLOWED_HOSTS`: vergul bilan ajrating, bo'sh joy yo'q!
- ✅ `CSRF_TRUSTED_ORIGINS`: `https://` bilan boshlang!
- ✅ `DATABASE_URL`: `${{Postgres.DATABASE_URL}}` aynan shunday yozing!
- ✅ Sizning Railway domain nomingizni yozing!

---

### Qadam 5: Git Push

```bash
git add .
git commit -m "Railway production ready"
git push origin main
```

Railway avtomatik deploy qiladi!

---

### Qadam 6: Logs Tekshirish

Railway dashboard → **Deployments** → **View logs**

**Muvaffaqiyatli deploy**:
```
✅ Starting Dastyor Backend...
✅ Waiting for database...
✅ Database is ready!
✅ Running migrations...
✅ Creating admin user...
✅ Admin user "admin" created successfully!
📧 Email: admin@dastyormenu.uz
🔑 Password: YourSecurePassword123!
✅ Collecting static files...
✅ Starting server...
✅ Listening on TCP address 0.0.0.0:8080
```

**Agar xato bo'lsa**:
```
❌ DisallowedHost: Invalid HTTP_HOST header
```
→ `ALLOWED_HOSTS` ni tekshiring!

```
❌ CSRF verification failed
```
→ `CSRF_TRUSTED_ORIGINS` ni tekshiring!

```
❌ could not connect to server
```
→ PostgreSQL service qo'shilganini tekshiring!

---

### Qadam 7: Test Qilish

#### 1. Swagger UI

```
https://dastyormenu-backend-production.up.railway.app/
```

Ko'rinishi kerak:
- ✅ Swagger UI sahifasi
- ✅ Barcha API endpoints
- ✅ "Try it out" tugmalari

#### 2. Admin Panel

```
https://dastyormenu-backend-production.up.railway.app/admin/
```

Login:
- **Username**: `admin` (yoki sizning `ADMIN_USERNAME`)
- **Password**: `YourSecurePassword123!` (yoki sizning `ADMIN_PASSWORD`)

Ko'rinishi kerak:
- ✅ Django admin login sahifasi
- ✅ Login qilish ishlaydi
- ✅ Admin dashboard

#### 3. API Test (Swagger UI da)

1. **POST /api/auth/login/** ni oching
2. **Try it out** bosing
3. Ma'lumot kiriting:
```json
{
  "login": "admin",
  "password": "YourSecurePassword123!"
}
```
4. **Execute** bosing

**Natija**:
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "username": "admin",
    "email": "admin@dastyormenu.uz",
    "role": "admin"
  }
}
```

---

## 🔧 Railway Variables - To'liq Ro'yxat

| Variable | Qiymat | Tavsif | Majburiy? |
|----------|--------|--------|-----------|
| `SECRET_KEY` | `generate_secret_key.py` dan | Django secret key | ✅ Ha |
| `DEBUG` | `False` | Debug mode | ✅ Ha |
| `DJANGO_SETTINGS_MODULE` | `config.settings.production` | Settings module | ✅ Ha |
| `ALLOWED_HOSTS` | `your-app.up.railway.app,.railway.app` | Ruxsat etilgan hostlar | ✅ Ha |
| `CSRF_TRUSTED_ORIGINS` | `https://your-app.up.railway.app` | CSRF trusted origins | ✅ Ha |
| `DATABASE_URL` | `${{Postgres.DATABASE_URL}}` | Database connection | ✅ Ha |
| `ADMIN_USERNAME` | `admin` | Admin username | ⚠️ Tavsiya |
| `ADMIN_EMAIL` | `admin@example.com` | Admin email | ⚠️ Tavsiya |
| `ADMIN_PASSWORD` | `admin123` | Admin password | ⚠️ Tavsiya |
| `CORS_ALLOWED_ORIGINS` | `https://yourdomain.com` | Frontend domain | ❌ Optional |
| `REDIS_URL` | `${{Redis.REDIS_URL}}` | Redis connection | ❌ Optional |

---

## 🐛 Troubleshooting

### 1. ALLOWED_HOSTS Xatosi

**Xato**:
```
DisallowedHost: Invalid HTTP_HOST header: 'your-app.up.railway.app'
```

**Yechim**:
1. Railway → **Variables** → `ALLOWED_HOSTS` ni tekshiring
2. Domain nomini to'g'ri yozganingizni tekshiring
3. Vergul bilan ajratilganini tekshiring (bo'sh joy yo'q!)
4. Masalan: `app1.railway.app,app2.railway.app`
5. Redeploy qiling

### 2. CSRF Xatosi

**Xato**:
```
CSRF verification failed. Request aborted.
```

**Yechim**:
1. Railway → **Variables** → `CSRF_TRUSTED_ORIGINS` ni tekshiring
2. `https://` bilan boshlanishini tekshiring
3. Domain nomini to'g'ri yozganingizni tekshiring
4. Masalan: `https://your-app.up.railway.app`
5. Redeploy qiling

### 3. Database Connection Xatosi

**Xato**:
```
could not connect to server: Connection refused
```

**Yechim**:
1. Railway → **+ New** → **Database** → **PostgreSQL** qo'shing
2. Variables da `DATABASE_URL=${{Postgres.DATABASE_URL}}` borligini tekshiring
3. Redeploy qiling

### 4. Admin User Yaratilmadi

**Xato**:
```
No such user: admin
```

**Yechim**:
1. Logs da "Creating admin user..." ni qidiring
2. Agar xato bo'lsa, `ADMIN_USERNAME`, `ADMIN_EMAIL`, `ADMIN_PASSWORD` tekshiring
3. Railway CLI bilan manual yaratish:

```bash
# Railway CLI o'rnatish
npm install -g @railway/cli

# Login
railway login

# Project link
railway link

# Django shell
railway run python manage.py createsuperuser
```

### 5. Static Files 404

**Xato**:
```
GET /static/admin/css/base.css 404
```

**Yechim**:
1. Logs da "Collecting static files..." ni qidiring
2. `requirements.txt` da `whitenoise==6.6.0` borligini tekshiring
3. Redeploy qiling

### 6. 500 Internal Server Error

**Yechim**:
1. Railway → **Deployments** → **View logs**
2. Xato xabarini o'qing
3. Agar `SECRET_KEY` xatosi bo'lsa, `SECRET_KEY` ni tekshiring
4. Agar `DATABASE_URL` xatosi bo'lsa, PostgreSQL service qo'shilganini tekshiring

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

Deploy qilishdan oldin:

- [ ] `SECRET_KEY` yaratildi (`python scripts/generate_secret_key.py`)
- [ ] Railway project yaratildi
- [ ] PostgreSQL service qo'shildi
- [ ] Railway domain nomi topildi (Settings → Domains)
- [ ] **BARCHA** environment variables qo'shildi:
  - [ ] `SECRET_KEY` (50+ characters)
  - [ ] `DEBUG=False`
  - [ ] `DJANGO_SETTINGS_MODULE=config.settings.production`
  - [ ] `ALLOWED_HOSTS` (sizning domain nomingiz!)
  - [ ] `CSRF_TRUSTED_ORIGINS` (https:// bilan!)
  - [ ] `DATABASE_URL=${{Postgres.DATABASE_URL}}`
  - [ ] `ADMIN_USERNAME` (optional)
  - [ ] `ADMIN_EMAIL` (optional)
  - [ ] `ADMIN_PASSWORD` (optional)
- [ ] Git push qilindi (`git push origin main`)
- [ ] Railway deploy qilindi (avtomatik)
- [ ] Logs tekshirildi (xatolar yo'q)
- [ ] Swagger UI ochildi (/)
- [ ] Admin panelga kirish test qilindi (/admin/)
- [ ] API login test qilindi (POST /api/auth/login/)

---

## 🎉 Muvaffaqiyatli Deploy!

Agar barcha qadamlar to'g'ri bajarilgan bo'lsa:

✅ **Swagger UI**: https://your-app.up.railway.app/
✅ **Admin Panel**: https://your-app.up.railway.app/admin/
✅ **API**: https://your-app.up.railway.app/api/

**Admin Login**:
- Username: `admin`
- Password: `YourSecurePassword123!`

⚠️ **Xavfsizlik**: Birinchi login qilgandan keyin admin parolni o'zgartiring!

---

## 📞 Keyingi Qadamlar

### 1. Admin Parolni O'zgartirish

1. Admin panelga kiring: `/admin/`
2. O'ng yuqori burchakda **Change password**
3. Yangi parolni kiriting
4. Saqlang

### 2. Custom Domain Qo'shish (Optional)

1. Railway → **Settings** → **Domains** → **Add Domain**
2. DNS sozlash (CNAME record)
3. Variables yangilash:
```bash
ALLOWED_HOSTS=yourdomain.com,.railway.app
CSRF_TRUSTED_ORIGINS=https://yourdomain.com
```

### 3. Redis Qo'shish (Optional, Celery uchun)

1. Railway → **+ New** → **Database** → **Redis**
2. Variables qo'shish:
```bash
REDIS_URL=${{Redis.REDIS_URL}}
CELERY_BROKER_URL=${{Redis.REDIS_URL}}/0
CELERY_RESULT_BACKEND=${{Redis.REDIS_URL}}/0
```

### 4. S3 Storage (Optional, rasm yuklash uchun)

1. AWS S3 bucket yaratish
2. Variables qo'shish:
```bash
USE_S3=True
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_STORAGE_BUCKET_NAME=your_bucket_name
AWS_S3_REGION_NAME=us-east-1
```

### 5. Monitoring

Railway → **Metrics**:
- CPU usage
- Memory usage
- Network traffic
- Request count

---

## 📚 Qo'shimcha Dokumentatsiya

- **RAILWAY_COMPLETE_GUIDE.md** - To'liq qo'llanma
- **RAILWAY_QUICK_FIX.md** - Tezkor yechim
- **RAILWAY_AUTO_ADMIN.md** - Admin user yaratish
- **FINAL_SUMMARY.md** - Umumiy xulosa

---

## 💡 Maslahatlar

1. **SECRET_KEY ni xavfsiz saqlang**: Hech qachon Git ga commit qilmang!
2. **Admin parolni o'zgartiring**: Default parol xavfsiz emas!
3. **Logs ni tekshiring**: Har deploy qilganda logs ni o'qing
4. **Backup qiling**: Railway avtomatik backup qiladi, lekin qo'shimcha backup ham yaxshi
5. **Monitoring qiling**: Railway Metrics dan foydalaning

---

Omad! 🚀 Agar savollar bo'lsa, so'rang! 💪
