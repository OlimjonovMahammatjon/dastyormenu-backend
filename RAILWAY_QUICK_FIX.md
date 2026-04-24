# ⚡ Railway Tezkor Yechim - ALLOWED_HOSTS Xatosi

## ❌ Xato

```
DisallowedHost: Invalid HTTP_HOST header: 'dastyormenu-backend-production.up.railway.app'
```

## ✅ Yechim (3 Qadam)

### 1️⃣ SECRET_KEY Yaratish

```bash
python scripts/generate_secret_key.py
```

Natijani nusxa oling! Masalan:
```
SECRET_KEY=:2KHj@gbyeN3>0SE!QsM-%.O`Hjg!tQ@0vCx7)!etO9se(,*l3
```

---

### 2️⃣ Railway Variables Qo'shish

Railway dashboard → **Variables** → **+ New Variable**

**DIQQAT**: Sizning Railway domain nomingizni kiriting! (masalan: `dastyormenu-backend-production.up.railway.app`)

```bash
SECRET_KEY=:2KHj@gbyeN3>0SE!QsM-%.O`Hjg!tQ@0vCx7)!etO9se(,*l3
DEBUG=False
DJANGO_SETTINGS_MODULE=config.settings.production
ALLOWED_HOSTS=dastyormenu-backend-production.up.railway.app,.railway.app
CSRF_TRUSTED_ORIGINS=https://dastyormenu-backend-production.up.railway.app
DATABASE_URL=${{Postgres.DATABASE_URL}}
ADMIN_USERNAME=admin
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=admin123
```

**MUHIM**: 
- `ALLOWED_HOSTS` da vergul bilan ajrating, bo'sh joy yo'q!
- `CSRF_TRUSTED_ORIGINS` da `https://` bilan boshlang!
- Sizning Railway domain nomingizni yozing!

---

### 3️⃣ Redeploy

```bash
git add .
git commit -m "Fixed ALLOWED_HOSTS"
git push origin main
```

Railway avtomatik deploy qiladi!

---

## 🔍 Domain Nomini Topish

Agar domain nomingizni bilmasangiz:

1. Railway dashboard → **Settings** → **Domains**
2. Domain nomini ko'ring (masalan: `your-app.up.railway.app`)
3. Variables da o'zgartiring:

```bash
ALLOWED_HOSTS=your-app.up.railway.app,.railway.app
CSRF_TRUSTED_ORIGINS=https://your-app.up.railway.app
```

---

## ✅ Test Qilish

Deploy tugagandan keyin:

**Swagger UI**: https://your-app.up.railway.app/
**Admin Panel**: https://your-app.up.railway.app/admin/

Login:
- Username: `admin`
- Password: `admin123`

---

## 🐛 Hali Ham Ishlamasa?

### 1. Variables Tekshirish

Railway → **Variables** → Quyidagilar borligini tekshiring:
- ✅ `ALLOWED_HOSTS` (vergul bilan ajratilgan, bo'sh joy yo'q)
- ✅ `CSRF_TRUSTED_ORIGINS` (https:// bilan)
- ✅ `DATABASE_URL` (${{Postgres.DATABASE_URL}})
- ✅ `SECRET_KEY` (50+ characters)

### 2. Logs Tekshirish

Railway → **Deployments** → **View logs**

Qidiring:
```
✅ Starting server...
✅ Listening on TCP address 0.0.0.0:8080
```

Agar xato bo'lsa:
```
❌ DisallowedHost: Invalid HTTP_HOST header
```

Bu `ALLOWED_HOSTS` to'g'ri sozlanmaganligini bildiradi!

### 3. PostgreSQL Tekshirish

Railway → **+ New** → **Database** → **PostgreSQL**

Agar hali qo'shilmagan bo'lsa, qo'shing!

---

## 📋 To'liq Variables Ro'yxati

| Variable | Qiymat | Majburiy? |
|----------|--------|-----------|
| `SECRET_KEY` | `generate_secret_key.py` dan | ✅ |
| `DEBUG` | `False` | ✅ |
| `DJANGO_SETTINGS_MODULE` | `config.settings.production` | ✅ |
| `ALLOWED_HOSTS` | `your-app.up.railway.app,.railway.app` | ✅ |
| `CSRF_TRUSTED_ORIGINS` | `https://your-app.up.railway.app` | ✅ |
| `DATABASE_URL` | `${{Postgres.DATABASE_URL}}` | ✅ |
| `ADMIN_USERNAME` | `admin` | ⚠️ |
| `ADMIN_EMAIL` | `admin@example.com` | ⚠️ |
| `ADMIN_PASSWORD` | `admin123` | ⚠️ |

---

## 🎉 Tayyor!

Agar barcha qadamlar to'g'ri bajarilgan bo'lsa, loyihangiz ishlaydi! 🚀

**Keyingi qadam**: Admin panelga kirib, parolni o'zgartiring!

Omad! 💪
