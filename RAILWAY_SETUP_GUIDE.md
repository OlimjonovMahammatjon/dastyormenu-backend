# 🚂 Railway Setup - Bosqichma-bosqich Qo'llanma

## ⚠️ MUHIM: Railway da PostgreSQL Service Kerak!

Xatolik:
```
DATABASE_URL not set, skipping database check
connection to server at "127.0.0.1", port 5432 failed
```

**Sabab**: Railway da PostgreSQL service yaratilmagan yoki `DATABASE_URL` o'rnatilmagan.

## 📋 To'liq Setup Jarayoni

### 1. Railway Account va Project

1. **Railway.app** ga kiring: https://railway.app
2. GitHub bilan login qiling
3. **New Project** tugmasini bosing
4. **Deploy from GitHub repo** ni tanlang
5. Repository ni tanlang va **Deploy Now** bosing

### 2. PostgreSQL Service Qo'shish (MAJBURIY!)

Railway project ochilgandan keyin:

1. **+ New** tugmasini bosing (o'ng yuqori burchakda)
2. **Database** ni tanlang
3. **Add PostgreSQL** ni bosing
4. PostgreSQL service yaratiladi (1-2 daqiqa)

✅ PostgreSQL service yaratilgandan keyin avtomatik ravishda quyidagi variables yaratiladi:
- `PGHOST`
- `PGPORT`
- `PGUSER`
- `PGPASSWORD`
- `PGDATABASE`
- `DATABASE_URL` ⭐ (Bu eng muhimi!)

### 3. Redis Service Qo'shish (Celery uchun)

1. **+ New** tugmasini bosing
2. **Database** ni tanlang
3. **Add Redis** ni bosing
4. Redis service yaratiladi

✅ Redis service yaratilgandan keyin:
- `REDIS_URL`
- `REDIS_HOST`
- `REDIS_PORT`

### 4. Environment Variables Sozlash

Django service ni tanlang va **Variables** bo'limiga o'ting:

#### A. Django Variables (Qo'lda qo'shish kerak)

```bash
# Django Core
SECRET_KEY=your-super-secret-key-change-this-in-production-min-50-chars
DEBUG=False
DJANGO_SETTINGS_MODULE=config.settings.production
ALLOWED_HOSTS=.railway.app

# CORS & CSRF (Frontend domain bilan)
CORS_ALLOWED_ORIGINS=https://your-frontend.vercel.app,https://your-app.railway.app
CSRF_TRUSTED_ORIGINS=https://your-frontend.vercel.app,https://your-app.railway.app

# Security
SECURE_SSL_REDIRECT=True

# App
BASE_URL=https://your-app.railway.app
PORT=8000
```

#### B. Database Variables (Avtomatik - Reference qilish)

Railway da PostgreSQL service yaratilgandan keyin, Django service da:

1. **Variables** bo'limiga o'ting
2. **+ New Variable** bosing
3. **Variable Reference** ni tanlang
4. Quyidagilarni qo'shing:

```bash
DATABASE_URL=${{Postgres.DATABASE_URL}}
```

Yoki to'liq:
```bash
DATABASE_URL=${{Postgres.DATABASE_URL}}
DB_NAME=${{Postgres.PGDATABASE}}
DB_USER=${{Postgres.PGUSER}}
DB_PASSWORD=${{Postgres.PGPASSWORD}}
DB_HOST=${{Postgres.PGHOST}}
DB_PORT=${{Postgres.PGPORT}}
```

**MUHIM**: `${{Postgres.DATABASE_URL}}` - bu Railway syntax. `Postgres` - bu sizning PostgreSQL service nomingiz. Agar boshqa nom bergan bo'lsangiz, o'sha nomni ishlating.

#### C. Redis Variables (Avtomatik - Reference qilish)

```bash
REDIS_URL=${{Redis.REDIS_URL}}
CELERY_BROKER_URL=${{Redis.REDIS_URL}}/0
CELERY_RESULT_BACKEND=${{Redis.REDIS_URL}}/0
```

### 5. Deploy Settings Tekshirish

Django service da **Settings** bo'limiga o'ting:

#### Build Settings
- **Builder**: NIXPACKS (avtomatik)
- **Build Command**: (bo'sh qoldiring)

#### Deploy Settings
- **Start Command**: `bash scripts/start.sh`
- **Restart Policy**: ON_FAILURE
- **Max Retries**: 10

Agar `railway.toml` fayl mavjud bo'lsa, Railway avtomatik o'qiydi.

### 6. Deploy!

1. **Deploy** tugmasini bosing (yoki avtomatik deploy)
2. **Deployments** bo'limida logs ni kuzating
3. Quyidagi jarayonni ko'rasiz:

```
Starting Dastyor Backend...
Waiting for database...
Database is ready!
Running migrations...
Operations to perform:
  Apply all migrations: ...
Running migrations:
  Applying contenttypes.0001_initial... OK
  ...
Collecting static files...
...
Starting server...
2024-04-24 09:00:00 [INFO] Listening on 0.0.0.0:8000
```

### 7. Domain va URL

Deploy tugagandan keyin:

1. **Settings** → **Networking**
2. Railway sizga domain beradi: `your-app.railway.app`
3. Custom domain qo'shishingiz mumkin

## 🔍 Troubleshooting

### Muammo 1: DATABASE_URL not set

**Xatolik**:
```
DATABASE_URL not set, skipping database check
connection to server at "127.0.0.1", port 5432 failed
```

**Yechim**:
1. PostgreSQL service yaratilganini tekshiring
2. Django service da `DATABASE_URL` variable mavjudligini tekshiring
3. Variable reference to'g'ri: `${{Postgres.DATABASE_URL}}`

**Tekshirish**:
```bash
# Railway CLI bilan
railway variables

# Yoki dashboard da Variables bo'limini ko'ring
```

### Muammo 2: Service nomi noto'g'ri

**Xatolik**: `${{Postgres.DATABASE_URL}}` ishlamayapti

**Yechim**:
1. PostgreSQL service nomini tekshiring (Railway dashboard)
2. Agar nom boshqa bo'lsa, masalan `PostgreSQL`, u holda:
   ```bash
   DATABASE_URL=${{PostgreSQL.DATABASE_URL}}
   ```

### Muammo 3: Migrations fail

**Xatolik**: Migrations bajarilmayapti

**Yechim**:
```bash
# Railway shell da
railway run python manage.py migrate

# Yoki logs ni ko'ring
railway logs
```

### Muammo 4: Static files 404

**Xatolik**: CSS/JS files topilmayapti

**Yechim**:
1. `collectstatic` bajarilganini tekshiring (logs da)
2. WhiteNoise middleware sozlanganini tekshiring
3. `STATIC_ROOT` to'g'ri sozlanganini tekshiring

## 📊 Railway Services Tuzilishi

```
┌─────────────────────────────────────┐
│  Django Service (Main)              │
│  - Web server (Daphne)              │
│  - Environment variables            │
│  - Domain: your-app.railway.app     │
└─────────────────────────────────────┘
           │
           ├─────────────────────────┐
           │                         │
┌──────────▼──────────┐   ┌─────────▼──────────┐
│  PostgreSQL         │   │  Redis             │
│  - DATABASE_URL     │   │  - REDIS_URL       │
│  - Auto backups     │   │  - Cache & Celery  │
└─────────────────────┘   └────────────────────┘
```

## 🎯 Minimal Environment Variables

Railway da **MINIMAL** kerakli variables:

```bash
# Django service da
SECRET_KEY=your-secret-key-min-50-chars
DEBUG=False
DJANGO_SETTINGS_MODULE=config.settings.production
DATABASE_URL=${{Postgres.DATABASE_URL}}
```

Qolgan hamma narsa optional!

## ✅ Deploy Success Belgilari

Logs da quyidagilarni ko'rishingiz kerak:

```
✅ Starting Dastyor Backend...
✅ Waiting for database...
✅ Database is ready!
✅ Running migrations...
✅ Applying contenttypes.0001_initial... OK
✅ Applying auth.0001_initial... OK
✅ ... (barcha migrations)
✅ Collecting static files...
✅ 150 static files copied to '/app/staticfiles'
✅ Starting server...
✅ Listening on 0.0.0.0:8000
```

## 🚀 Deploy Qilish (Git Push)

```bash
# Local da o'zgarishlar
git add .
git commit -m "Railway deployment ready"
git push origin main

# Railway avtomatik deploy qiladi
```

## 📱 API Test Qilish

Deploy tugagandan keyin:

```bash
# Health check
curl https://your-app.railway.app/api/

# Swagger UI
https://your-app.railway.app/api/docs/

# Login test
curl -X POST https://your-app.railway.app/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"login":"manager@test.com","password":"password123"}'
```

## 🔐 Security Checklist

- [ ] `SECRET_KEY` o'zgartirildi (min 50 chars)
- [ ] `DEBUG=False`
- [ ] `ALLOWED_HOSTS` to'g'ri sozlandi
- [ ] `CORS_ALLOWED_ORIGINS` frontend domain bilan
- [ ] `CSRF_TRUSTED_ORIGINS` frontend domain bilan
- [ ] `SECURE_SSL_REDIRECT=True`
- [ ] PostgreSQL service yaratildi
- [ ] `DATABASE_URL` reference qilindi
- [ ] Redis service yaratildi (agar Celery kerak bo'lsa)

## 📚 Qo'shimcha Services

### Celery Worker (Optional)

Agar background tasks kerak bo'lsa:

1. **+ New** → **Empty Service**
2. Xuddi shu GitHub repo ni tanlang
3. **Variables** da Django service variables ni copy qiling
4. **Settings** → **Deploy**:
   - Start Command: `celery -A config worker -l info`
5. Deploy

### Celery Beat (Optional)

Periodic tasks uchun:

1. **+ New** → **Empty Service**
2. Xuddi shu repo
3. Variables copy
4. Start Command: `celery -A config beat -l info`

## 🎉 Yakuniy Natija

Agar hammasi to'g'ri bo'lsa:

- ✅ Django API: `https://your-app.railway.app/api/`
- ✅ Swagger UI: `https://your-app.railway.app/api/docs/`
- ✅ Admin Panel: `https://your-app.railway.app/admin/`
- ✅ PostgreSQL: Ishlayapti
- ✅ Redis: Ishlayapti (agar qo'shgan bo'lsangiz)
- ✅ Static Files: Serve qilinmoqda
- ✅ HTTPS: Avtomatik

Omad! 🚀
