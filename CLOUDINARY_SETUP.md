# Cloudinary Setup Guide - Rasmlarni Professional Tarzda Sozlash

## 1. Cloudinary Account Yaratish

1. [Cloudinary](https://cloudinary.com) saytiga kiring
2. **Sign Up for Free** tugmasini bosing
3. Email, parol va ismingizni kiriting
4. Accountni tasdiqlang

**FREE PLAN:**
- 25 GB storage
- 25 GB bandwidth/oy
- 25,000 transformations/oy
- Bu ko'pchilik loyihalar uchun yetarli!

## 2. Cloudinary Credentials Olish

1. Cloudinary Dashboard'ga kiring: https://console.cloudinary.com
2. Dashboard'da **Account Details** bo'limini toping
3. Quyidagi ma'lumotlarni ko'chirib oling:
   - **Cloud Name** (masalan: `dz1a2b3c4`)
   - **API Key** (masalan: `123456789012345`)
   - **API Secret** (masalan: `abcdefghijklmnopqrstuvwxyz123`)

## 3. .env Faylini Yangilash

`.env` faylingizni oching va quyidagi qatorlarni o'zgartiring:

```bash
# Cloudinary (Production Image Storage)
USE_CLOUDINARY=True
CLOUDINARY_CLOUD_NAME=sizning-cloud-name
CLOUDINARY_API_KEY=sizning-api-key
CLOUDINARY_API_SECRET=sizning-api-secret
```

**MUHIM:** `your-cloud-name`, `your-api-key`, `your-api-secret` o'rniga o'zingizning haqiqiy ma'lumotlaringizni yozing!

## 4. Production (Railway) uchun Environment Variables

Railway dashboard'da:

1. **Variables** bo'limiga kiring
2. Quyidagi o'zgaruvchilarni qo'shing:

```
USE_CLOUDINARY=True
CLOUDINARY_CLOUD_NAME=sizning-cloud-name
CLOUDINARY_API_KEY=sizning-api-key
CLOUDINARY_API_SECRET=sizning-api-secret
```

## 5. Serverni Qayta Ishga Tushirish

### Local Development:
```bash
# Serverni to'xtating (Ctrl+C)
# Qayta ishga tushiring
python manage.py runserver
```

### Railway Production:
```bash
# Railway avtomatik deploy qiladi yoki:
railway up
```

## 6. Rasmlarni Test Qilish

### Admin Panel orqali:
1. http://localhost:8000/admin/ ga kiring
2. **Menu items** yoki **Organizations** ga o'ting
3. Yangi rasm yuklang
4. Rasm Cloudinary'ga yuklanadi va URL avtomatik yaratiladi

### API orqali:
```bash
# Menu item yaratish (rasm bilan)
curl -X POST http://localhost:8000/api/menu/items/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "name=Osh" \
  -F "price=2500000" \
  -F "category=CATEGORY_UUID" \
  -F "image_url=@/path/to/image.jpg"
```

## 7. Cloudinary Dashboard'da Rasmlarni Ko'rish

1. https://console.cloudinary.com/console/media_library ga kiring
2. **Media Library** bo'limida barcha yuklangan rasmlarni ko'rasiz
3. Rasmlar quyidagi papkalarda saqlanadi:
   - `menu/items/` - Menu rasmlari
   - `organizations/logos/` - Restaurant logolari

## 8. Rasm URL Formati

Cloudinary rasmlar quyidagi formatda bo'ladi:

```
https://res.cloudinary.com/YOUR_CLOUD_NAME/image/upload/v1234567890/menu/items/filename.jpg
```

**Afzalliklari:**
- ✅ Global CDN - tez yuklanish
- ✅ Avtomatik optimizatsiya
- ✅ Responsive images
- ✅ Format konvertatsiya (WebP, AVIF)
- ✅ Lazy loading support
- ✅ Image transformations (resize, crop, filters)

## 9. Mavjud Rasmlarni Cloudinary'ga Ko'chirish

Agar sizda allaqachon local rasmlar bo'lsa:

```bash
# Migration script ishga tushiring
python migrate_images_to_cloudinary.py
```

Bu script barcha local rasmlarni Cloudinary'ga ko'chiradi.

## 10. Troubleshooting

### Rasm yuklanmayapti:
```bash
# Cloudinary credentials'ni tekshiring
python manage.py shell
>>> from django.conf import settings
>>> print(settings.USE_CLOUDINARY)  # True bo'lishi kerak
>>> print(settings.CLOUDINARY_STORAGE)  # Ma'lumotlar to'g'ri bo'lishi kerak
```

### Rasm URL'i noto'g'ri:
- Serializer'da `context={'request': request}` o'tkazilganini tekshiring
- ViewSet'da `get_serializer_context()` to'g'ri ishlayotganini tekshiring

### Cloudinary'ga ulanish xatosi:
```bash
# Credentials'ni test qiling
python manage.py shell
>>> import cloudinary
>>> cloudinary.config(
...     cloud_name='YOUR_CLOUD_NAME',
...     api_key='YOUR_API_KEY',
...     api_secret='YOUR_API_SECRET'
... )
>>> cloudinary.api.ping()  # {'status': 'ok'} qaytarishi kerak
```

## 11. Best Practices

### Rasm Optimizatsiyasi:
```python
# Cloudinary URL'da transformatsiyalar
# Avtomatik format va quality
image_url = "https://res.cloudinary.com/YOUR_CLOUD_NAME/image/upload/f_auto,q_auto/menu/items/image.jpg"

# Responsive sizes
thumbnail = "https://res.cloudinary.com/YOUR_CLOUD_NAME/image/upload/w_200,h_200,c_fill/menu/items/image.jpg"
medium = "https://res.cloudinary.com/YOUR_CLOUD_NAME/image/upload/w_800,h_600,c_fit/menu/items/image.jpg"
```

### Security:
- ❌ API Secret'ni hech qachon frontend'ga yubormang
- ✅ Faqat backend'da ishlating
- ✅ Environment variables'da saqlang
- ✅ .gitignore'ga .env qo'shing

## 12. Monitoring

Cloudinary Dashboard'da:
- **Usage** - bandwidth va storage
- **Transformations** - optimization statistikasi
- **Media Library** - barcha rasmlar
- **Reports** - detailed analytics

---

## Qo'shimcha Yordam

Agar muammo bo'lsa:
1. Cloudinary documentation: https://cloudinary.com/documentation/django_integration
2. Django-cloudinary-storage: https://github.com/klis87/django-cloudinary-storage
3. Support: support@cloudinary.com

**Muvaffaqiyatli sozlash!** 🎉
