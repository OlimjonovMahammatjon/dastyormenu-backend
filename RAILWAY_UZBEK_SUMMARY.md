# 🎯 Railway Deploy - O'zbek Tilida Qisqacha

## ❌ Muammo

Railway da admin panelga kirishda xato:
```
DisallowedHost: Invalid HTTP_HOST header
```

## ✅ Yechim

### 1. SECRET_KEY Yaratish

Terminal da:
```bash
python scripts/generate_secret_key.py
```

Natijani nusxa oling!

---

### 2. Railway Variables

Railway dashboard → **Variables** → **+ New Variable**

**DIQQAT**: `dastyormenu-backend-production.up.railway.app` o'rniga **sizning Railway domain nomingizni** yozing!

Domain nomini topish: Railway → **Settings** → **Domains**

```bash
SECRET_KEY=:2KHj@gbyeN3>0SE!QsM-%.O`Hjg!tQ@0vCx7)!etO9se(,*l3
DEBUG=False
DJANGO_SETTINGS_MODULE=config.settings.production
ALLOWED_HOSTS=dastyormenu-backend-production.up.railway.app,.railway.app
CSRF_TRUSTED_ORIGINS=https://dastyormenu-backend-production.up.railway.app
DATABASE_URL=${{Postgres.DATABASE_URL}}
ADMIN_USERNAME=admin
ADMIN_EMAIL=admin@dastyormenu.uz
ADMIN_PASSWORD=admin123
```

**Muhim**:
- `ALLOWED_HOSTS`: vergul bilan ajrating, bo'sh joy yo'q!
- `CSRF_TRUSTED_ORIGINS`: `https://` bilan boshlang!
- Sizning domain nomingizni yozing!

---

### 3. Git Push

```bash
git add .
git commit -m "Railway production ready"
git push origin main
```

Railway avtomatik deploy qiladi!

---

### 4. Test Qilish

**Swagger UI**: https://your-app.up.railway.app/
**Admin Panel**: https://your-app.up.railway.app/admin/

Login:
- Username: `admin`
- Password: `admin123`

---

## 🐛 Hali Ham Ishlamasa?

### 1. Variables Tekshirish

Railway → **Variables** → Quyidagilar borligini tekshiring:
- ✅ `ALLOWED_HOSTS` (sizning domain nomingiz!)
- ✅ `CSRF_TRUSTED_ORIGINS` (https:// bilan!)
- ✅ `DATABASE_URL` (${{Postgres.DATABASE_URL}})
- ✅ `SECRET_KEY` (50+ characters)

### 2. PostgreSQL Qo'shish

Railway → **+ New** → **Database** → **PostgreSQL**

### 3. Logs Tekshirish

Railway → **Deployments** → **View logs**

Qidiring:
```
✅ Starting server...
✅ Listening on TCP address 0.0.0.0:8080
```

---

## 📋 Checklist

- [ ] SECRET_KEY yaratildi
- [ ] Railway project yaratildi
- [ ] PostgreSQL qo'shildi
- [ ] Domain nomi topildi
- [ ] BARCHA variables qo'shildi
- [ ] Git push qilindi
- [ ] Logs tekshirildi
- [ ] Admin panelga kirish test qilindi

---

## 🎉 Tayyor!

Agar barcha qadamlar to'g'ri bajarilgan bo'lsa, loyihangiz ishlaydi! 🚀

**Keyingi qadam**: Admin panelga kirib, parolni o'zgartiring!

---

## 📚 Batafsil Qo'llanmalar

- **RAILWAY_FINAL_INSTRUCTIONS.md** - To'liq ko'rsatmalar
- **RAILWAY_COMPLETE_GUIDE.md** - Batafsil qo'llanma
- **RAILWAY_QUICK_FIX.md** - Tezkor yechim

Omad! 💪
