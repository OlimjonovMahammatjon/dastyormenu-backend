# Cloudinary - Tezkor Boshlash 🚀

## 1. Cloudinary Account (2 daqiqa)

1. https://cloudinary.com ga kiring
2. **Sign Up for Free** - Email bilan ro'yxatdan o'ting
3. Email'ni tasdiqlang

## 2. Credentials Olish (1 daqiqa)

1. https://console.cloudinary.com ga kiring
2. Dashboard'da **Account Details** ni ko'ring
3. Ushbu 3 ta ma'lumotni ko'chirib oling:
   - **Cloud Name**
   - **API Key**
   - **API Secret**

## 3. .env Faylini Yangilash (1 daqiqa)

`.env` faylini oching va quyidagilarni o'zgartiring:

```bash
USE_CLOUDINARY=True
CLOUDINARY_CLOUD_NAME=sizning-cloud-name-bu-yerga
CLOUDINARY_API_KEY=sizning-api-key-bu-yerga
CLOUDINARY_API_SECRET=sizning-api-secret-bu-yerga
```

**MUHIM:** `your-cloud-name`, `your-api-key`, `your-api-secret` o'rniga **o'zingizning haqiqiy ma'lumotlaringizni** yozing!

## 4. Test Qilish (1 daqiqa)

```bash
# Cloudinary ulanishini test qiling
python test_cloudinary.py
```

Agar `✅ Everything is configured correctly!` ko'rsangiz - hammasi tayyor!

## 5. Serverni Qayta Ishga Tushirish

```bash
# Serverni to'xtating (Ctrl+C)
# Qayta ishga tushiring
python manage.py runserver
```

## 6. Rasm Yuklash

### Admin Panel orqali:
1. http://localhost:8000/admin/ ga kiring
2. **Menu items** ga o'ting
3. Yangi item yarating va rasm yuklang
4. Rasm avtomatik Cloudinary'ga yuklanadi! ✅

### API orqali:
```bash
curl -X POST http://localhost:8000/api/menu/items/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "name=Osh" \
  -F "price=2500000" \
  -F "category=CATEGORY_UUID" \
  -F "image_url=@/path/to/image.jpg"
```

## 7. Railway (Production) uchun

Railway dashboard'da **Variables** bo'limiga qo'shing:

```
USE_CLOUDINARY=True
CLOUDINARY_CLOUD_NAME=sizning-cloud-name
CLOUDINARY_API_KEY=sizning-api-key
CLOUDINARY_API_SECRET=sizning-api-secret
```

Deploy qiling va rasmlar avtomatik Cloudinary'dan yuklanadi!

## 8. Mavjud Rasmlarni Ko'chirish (Agar kerak bo'lsa)

```bash
python migrate_images_to_cloudinary.py
```

---

## ✅ Tayyor!

Endi barcha rasmlar:
- ☁️ Cloudinary CDN'da saqlanadi
- 🚀 Tez yuklanadi (global CDN)
- 🔄 Avtomatik optimizatsiya
- 📱 Responsive images
- 🆓 25GB bepul storage

## ❓ Muammo bo'lsa?

```bash
# Test qiling
python test_cloudinary.py

# Yoki
python manage.py shell
>>> from django.conf import settings
>>> print(settings.USE_CLOUDINARY)  # True bo'lishi kerak
```

**Batafsil qo'llanma:** `CLOUDINARY_SETUP.md` faylini o'qing

---

**Muvaffaqiyatli ishlar!** 🎉
