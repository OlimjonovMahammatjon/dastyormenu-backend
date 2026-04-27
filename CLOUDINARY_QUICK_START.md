# ⚡ Cloudinary Tezkor Boshlash

## 🎯 3 Qadam - 5 Daqiqa

### 1️⃣ Cloudinary Account (2 daqiqa)

1. https://cloudinary.com → **Sign Up**
2. Email tasdiqlang
3. Dashboard → **Account Details** → Credentials ni nusxa oling:
   - Cloud name: `your-cloud-name`
   - API Key: `123456789012345`
   - API Secret: `abcdefghijklmnopqrstuvwxyz`

---

### 2️⃣ Local Setup (1 daqiqa)

`.env` faylini yarating/yangilang:

```bash
USE_CLOUDINARY=True
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=123456789012345
CLOUDINARY_API_SECRET=abcdefghijklmnopqrstuvwxyz
```

**MUHIM**: O'zingizning credentials ni yozing!

---

### 3️⃣ Railway Setup (2 daqiqa)

Railway dashboard → **Variables** → **+ New Variable**:

```bash
USE_CLOUDINARY=True
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=123456789012345
CLOUDINARY_API_SECRET=abcdefghijklmnopqrstuvwxyz
```

Deploy:
```bash
git add .
git commit -m "Added Cloudinary"
git push origin main
```

---

## ✅ Tayyor!

Endi rasmlar:
- ✅ Cloudinary da saqlanadi
- ✅ Hech qachon o'chib ketmaydi
- ✅ Tez yuklash (CDN)
- ✅ Bepul 25GB

**Rasm URL**:
```
https://res.cloudinary.com/your-cloud-name/image/upload/menu/items/osh.jpg
```

---

## 🧪 Test

```bash
# Local
python manage.py runserver
# Admin panel → Menu → Add item → Upload image

# Railway
# Admin panel → Menu → Add item → Upload image
```

---

Batafsil: **CLOUDINARY_SETUP.md**

Omad! 🚀
