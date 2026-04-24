# ⚡ CORS Tezkor Yechim

## ❌ Xato

```
Access to fetch blocked by CORS policy
```

## ✅ Yechim (2 Qadam)

### 1️⃣ Railway Variables Qo'shish

Railway dashboard → **Variables** → **+ New Variable**:

**Test uchun** (barcha originlar):
```bash
# CORS_ALLOWED_ORIGINS ni qo'shmang
# Avtomatik barcha originlar ruxsat etiladi
```

**Production uchun** (aniq originlar - TAVSIYA):
```bash
CORS_ALLOWED_ORIGINS=http://localhost:5174,http://localhost:3000,https://yourdomain.com
```

**MUHIM**: 
- Vergul bilan ajrating, bo'sh joy yo'q!
- `http://` yoki `https://` bilan boshlang!
- Port raqamini kiriting!

---

### 2️⃣ Redeploy

```bash
git add .
git commit -m "Fixed CORS for Railway"
git push origin main
```

Railway avtomatik redeploy qiladi!

---

## 🧪 Test Qilish

Frontend da (http://localhost:5174):

```javascript
fetch('https://dastyormenu-backend-production.up.railway.app/api/auth/login/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ login: 'admin', password: 'admin123' })
})
.then(res => res.json())
.then(data => console.log('✅ Success:', data))
.catch(err => console.error('❌ Error:', err));
```

---

## 📋 To'liq Variables Ro'yxati

```bash
SECRET_KEY=:2KHj@gbyeN3>0SE!QsM-%.O`Hjg!tQ@0vCx7)!etO9se(,*l3
DEBUG=False
DJANGO_SETTINGS_MODULE=config.settings.production
ALLOWED_HOSTS=dastyormenu-backend-production.up.railway.app,.railway.app
CSRF_TRUSTED_ORIGINS=https://dastyormenu-backend-production.up.railway.app
DATABASE_URL=${{Postgres.DATABASE_URL}}
CORS_ALLOWED_ORIGINS=http://localhost:5174,https://yourdomain.com
ADMIN_USERNAME=admin
ADMIN_EMAIL=admin@dastyormenu.uz
ADMIN_PASSWORD=admin123
```

---

## 🐛 Hali Ham Ishlamasa?

### 1. Variables Tekshirish

```bash
# ✅ To'g'ri
CORS_ALLOWED_ORIGINS=http://localhost:5174,https://app.com

# ❌ Noto'g'ri (bo'sh joy bor)
CORS_ALLOWED_ORIGINS=http://localhost:5174, https://app.com

# ❌ Noto'g'ri (http:// yo'q)
CORS_ALLOWED_ORIGINS=localhost:5174
```

### 2. Logs Tekshirish

Railway → **Deployments** → **View logs**

Qidiring:
```
CORS_ALLOW_ALL_ORIGINS = True
```

### 3. Browser Cache Tozalash

- Browser cache ni tozalang
- Hard refresh: `Ctrl+Shift+R` (Windows) yoki `Cmd+Shift+R` (Mac)

---

## 🎉 Tayyor!

Agar barcha qadamlar to'g'ri bajarilgan bo'lsa, CORS xatosi yo'qoladi! 🚀

Batafsil: **RAILWAY_CORS_FIX.md**
