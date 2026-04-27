# 🚀 Railway → Cloudinary Migration

## ❌ Muammo

Railway da rasmlar yuklangan lekin ochilmayapti:
```
https://dastyormenu-backend-production.up.railway.app/media/menu/items/fc6dff45c75b6b434593b87167b30ef3.jpg
```

**Sabab**: Railway ephemeral filesystem - har deploy qilganda fayllar o'chib ketadi!

---

## ✅ Yechim: Cloudinary ga Ko'chirish

### Qadam 1: Cloudinary Account (2 daqiqa)

1. https://cloudinary.com → **Sign Up for Free**
2. Email tasdiqlang
3. Dashboard → **Account Details** → Credentials:
   - **Cloud name**: `dastyormenu` (yoki sizniki)
   - **API Key**: `123456789012345`
   - **API Secret**: `abcdefghijklmnopqrstuvwxyz`

**MUHIM**: Bu ma'lumotlarni nusxa oling!

---

### Qadam 2: Railway Variables Qo'shish

Railway dashboard → **Variables** → **+ New Variable**:

```bash
USE_CLOUDINARY=True
CLOUDINARY_CLOUD_NAME=dastyormenu
CLOUDINARY_API_KEY=123456789012345
CLOUDINARY_API_SECRET=abcdefghijklmnopqrstuvwxyz
```

**MUHIM**: O'zingizning credentials ni yozing!

---

### Qadam 3: Code Deploy

```bash
git add .
git commit -m "Added Cloudinary for permanent media storage"
git push origin main
```

Railway avtomatik deploy qiladi!

---

### Qadam 4: Mavjud Rasmlarni Ko'chirish

#### Variant A: Railway Shell Orqali (Tavsiya)

1. **Railway CLI o'rnatish**:
```bash
npm install -g @railway/cli
```

2. **Login**:
```bash
railway login
```

3. **Project link**:
```bash
railway link
```

4. **Migration script yuklash**:
```bash
railway run python migrate_images_to_cloudinary.py
```

#### Variant B: Local dan Ko'chirish

1. **Local .env sozlang**:
```bash
USE_CLOUDINARY=True
CLOUDINARY_CLOUD_NAME=dastyormenu
CLOUDINARY_API_KEY=123456789012345
CLOUDINARY_API_SECRET=abcdefghijklmnopqrstuvwxyz
```

2. **Migration script ishga tushiring**:
```bash
python migrate_images_to_cloudinary.py
```

**Natija**:
```
☁️  Cloudinary Migration Tool
============================================================
Cloud Name: dastyormenu
============================================================

🔄 Starting image migration to Cloudinary...

📋 Found 2 menu items with images

📸 Processing: Osh
   Current URL: https://dastyormenu-backend-production.up.railway.app/media/menu/items/fc6dff45c75b6b434593b87167b30ef3.jpg
   ✅ Migrated to: https://res.cloudinary.com/dastyormenu/image/upload/v1234567890/menu/items/fc6dff45c75b6b434593b87167b30ef3.jpg

📸 Processing: Lag'mon
   Current URL: https://dastyormenu-backend-production.up.railway.app/media/menu/items/8.png
   ✅ Migrated to: https://res.cloudinary.com/dastyormenu/image/upload/v1234567890/menu/items/8.png

============================================================
✅ Migration complete!
   Migrated: 2
   Failed: 0
   Total: 2
============================================================

🎉 All done! Images are now on Cloudinary.
```

---

### Qadam 5: Test Qilish

#### API Test

```bash
curl https://dastyormenu-backend-production.up.railway.app/api/menu/
```

**Natija**:
```json
{
  "id": "uuid",
  "name": "Osh",
  "image_url": "https://res.cloudinary.com/dastyormenu/image/upload/v1234567890/menu/items/fc6dff45c75b6b434593b87167b30ef3.jpg",
  "price": 2500000
}
```

✅ Rasm URL endi Cloudinary dan!

#### Browser Test

Rasm URL ni brauzerda oching:
```
https://res.cloudinary.com/dastyormenu/image/upload/v1234567890/menu/items/fc6dff45c75b6b434593b87167b30ef3.jpg
```

✅ Rasm ochilishi kerak!

---

## 🎯 Keyingi Rasmlar

Endi yangi rasmlar avtomatik Cloudinary ga yuklanadi:

1. **Admin panel** → Menu → Add item → Upload image
2. Rasm avtomatik Cloudinary ga yuklanadi
3. Database da Cloudinary URL saqlanadi

**Misol**:
```
https://res.cloudinary.com/dastyormenu/image/upload/v1234567890/menu/items/new-dish.jpg
```

---

## 📊 Cloudinary Dashboard

### Rasmlarni Ko'rish

1. Cloudinary dashboard → **Media Library**
2. Barcha rasmlaringizni ko'rasiz:
   - `menu/items/fc6dff45c75b6b434593b87167b30ef3.jpg`
   - `menu/items/8.png`
   - va boshqalar

### Storage

Dashboard → **Usage**:
- **Storage**: 2.5 MB / 25 GB
- **Bandwidth**: 10 MB / 25 GB
- **Transformations**: 5 / 25,000

---

## 🔧 Troubleshooting

### 1. Migration Script Xatosi

**Xato**: `cloudinary.exceptions.Error: Must supply api_key`

**Yechim**:
1. `.env` faylda Cloudinary credentials borligini tekshiring
2. `USE_CLOUDINARY=True` o'rnatilganini tekshiring
3. Credentials to'g'ri yozilganini tekshiring

### 2. Railway da Rasmlar Hali Ham Ochilmayapti

**Yechim**:
1. Railway Variables da Cloudinary credentials borligini tekshiring
2. `USE_CLOUDINARY=True` o'rnatilganini tekshiring
3. Redeploy qiling: `git push origin main`
4. Migration script ni qayta ishga tushiring

### 3. Ba'zi Rasmlar Ko'chirilmadi

**Yechim**:
1. Migration script logs ni tekshiring
2. Failed rasmlarni qo'lda admin panel orqali qayta yuklang
3. Yangi rasmlar avtomatik Cloudinary ga yuklanadi

---

## ✅ Checklist

- [ ] Cloudinary account yaratildi
- [ ] Cloud name, API key, API secret olindi
- [ ] Railway Variables qo'shildi:
  - [ ] `USE_CLOUDINARY=True`
  - [ ] `CLOUDINARY_CLOUD_NAME`
  - [ ] `CLOUDINARY_API_KEY`
  - [ ] `CLOUDINARY_API_SECRET`
- [ ] Code deploy qilindi (`git push`)
- [ ] Migration script ishga tushirildi
- [ ] API test qilindi (rasm URL Cloudinary dan)
- [ ] Browser da rasm ochildi

---

## 🎉 Natija

Endi:
- ✅ Barcha rasmlar Cloudinary da
- ✅ Rasmlar hech qachon o'chib ketmaydi
- ✅ Tez yuklash (CDN)
- ✅ Yangi rasmlar avtomatik Cloudinary ga yuklanadi
- ✅ Railway bilan mukammal ishlaydi

**Eski URL** (ishlamaydi):
```
https://dastyormenu-backend-production.up.railway.app/media/menu/items/fc6dff45c75b6b434593b87167b30ef3.jpg
```

**Yangi URL** (ishlaydi):
```
https://res.cloudinary.com/dastyormenu/image/upload/v1234567890/menu/items/fc6dff45c75b6b434593b87167b30ef3.jpg
```

---

## 💡 Qo'shimcha

### Rasm Transformatsiyalari

Cloudinary URL orqali rasm o'lchamini o'zgartirish:

**300x300 thumbnail**:
```
https://res.cloudinary.com/dastyormenu/image/upload/w_300,h_300,c_fill/menu/items/fc6dff45c75b6b434593b87167b30ef3.jpg
```

**800x600 optimized**:
```
https://res.cloudinary.com/dastyormenu/image/upload/w_800,h_600,c_fit,q_auto,f_auto/menu/items/fc6dff45c75b6b434593b87167b30ef3.jpg
```

### Avtomatik Optimizatsiya

Cloudinary avtomatik:
- ✅ WebP formatga konvertatsiya qiladi
- ✅ Rasmni siqadi (compression)
- ✅ Lazy loading qo'llab-quvvatlaydi
- ✅ CDN orqali serve qiladi

---

Omad! 🚀
