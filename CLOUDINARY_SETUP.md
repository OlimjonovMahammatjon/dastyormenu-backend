# ☁️ Cloudinary Setup - Rasmlar uchun Mukammal Yechim

## 🎯 Nega Cloudinary?

✅ **Bepul**: 25GB storage, 25GB bandwidth/month
✅ **Oson**: 5 daqiqada sozlash
✅ **Ishonchli**: Rasmlar hech qachon o'chib ketmaydi
✅ **Tez**: CDN orqali tez yuklash
✅ **Railway bilan mukammal**: Ephemeral filesystem muammosi yo'q

---

## 📝 Qadam 1: Cloudinary Account Yaratish

### 1. Ro'yxatdan O'tish

1. https://cloudinary.com ga kiring
2. **Sign Up for Free** bosing
3. Email, parol kiriting
4. Email ni tasdiqlang

### 2. Dashboard

Login qilgandan keyin Dashboard ga kirasiz:
- **Cloud name**: `your-cloud-name` (eslab qoling!)
- **API Key**: `123456789012345`
- **API Secret**: `abcdefghijklmnopqrstuvwxyz`

**MUHIM**: Bu ma'lumotlarni nusxa oling!

---

## 🔧 Qadam 2: Local Setup

### 1. Packages O'rnatildi ✅

```bash
pip install cloudinary django-cloudinary-storage
```

`requirements.txt` ga qo'shildi:
```txt
cloudinary==1.44.2
django-cloudinary-storage==0.3.0
```

### 2. Settings Sozlandi ✅

`config/settings/base.py` da:
```python
INSTALLED_APPS = [
    # ...
    'cloudinary_storage',
    'cloudinary',
    # ...
]

# Cloudinary Storage
USE_CLOUDINARY = os.getenv('USE_CLOUDINARY', 'False') == 'True'
if USE_CLOUDINARY:
    CLOUDINARY_STORAGE = {
        'CLOUD_NAME': os.getenv('CLOUDINARY_CLOUD_NAME'),
        'API_KEY': os.getenv('CLOUDINARY_API_KEY'),
        'API_SECRET': os.getenv('CLOUDINARY_API_SECRET'),
    }
    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
```

### 3. Local .env Fayl

`.env` faylini yarating yoki yangilang:

```bash
# Cloudinary
USE_CLOUDINARY=True
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=123456789012345
CLOUDINARY_API_SECRET=abcdefghijklmnopqrstuvwxyz
```

**MUHIM**: `your-cloud-name`, `API_KEY`, `API_SECRET` ni o'zingizniki bilan almashtiring!

---

## 🚀 Qadam 3: Railway Setup

### 1. Railway Variables Qo'shish

Railway dashboard → **Variables** → **+ New Variable**

```bash
USE_CLOUDINARY=True
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=123456789012345
CLOUDINARY_API_SECRET=abcdefghijklmnopqrstuvwxyz
```

### 2. Deploy

```bash
git add .
git commit -m "Added Cloudinary for media storage"
git push origin main
```

Railway avtomatik deploy qiladi!

---

## 🧪 Qadam 4: Test Qilish

### Local Test

1. **Server ishga tushiring**:
```bash
python manage.py runserver
```

2. **Admin panelga kiring**: http://localhost:8000/admin/

3. **Menu item yarating**:
   - Menu → Add menu item
   - Rasm yuklang
   - Save

4. **API dan tekshiring**:
```bash
curl http://localhost:8000/api/menu/
```

**Natija**:
```json
{
  "image_url": "https://res.cloudinary.com/your-cloud-name/image/upload/v1234567890/menu/items/abc123.jpg"
}
```

✅ Rasm URL Cloudinary dan keladi!

### Railway Test

1. **Deploy qiling**
2. **Admin panelga kiring**: https://your-app.railway.app/admin/
3. **Menu item yarating va rasm yuklang**
4. **API dan tekshiring**:
```bash
curl https://your-app.railway.app/api/menu/
```

✅ Rasmlar Cloudinary da saqlanadi va hech qachon o'chib ketmaydi!

---

## 📊 Cloudinary Dashboard

### Rasmlarni Ko'rish

1. Cloudinary dashboard → **Media Library**
2. Barcha yuklangan rasmlarni ko'rasiz
3. Har bir rasmni:
   - Ko'rish
   - Tahrirlash
   - O'chirish
   - URL olish

### Storage Statistikasi

Dashboard → **Usage**:
- **Storage**: 0.5 GB / 25 GB
- **Bandwidth**: 1.2 GB / 25 GB
- **Transformations**: 100 / 25,000

---

## 🎨 Cloudinary Imkoniyatlari

### 1. Avtomatik Optimizatsiya

Rasmlar avtomatik optimizatsiya qilinadi:
- WebP formatga konvertatsiya
- Siqish (compression)
- Lazy loading

### 2. Rasm Transformatsiyalari

URL orqali rasm o'lchamini o'zgartirish:

**Original**:
```
https://res.cloudinary.com/your-cloud-name/image/upload/menu/items/osh.jpg
```

**300x300 thumbnail**:
```
https://res.cloudinary.com/your-cloud-name/image/upload/w_300,h_300,c_fill/menu/items/osh.jpg
```

**Blur effect**:
```
https://res.cloudinary.com/your-cloud-name/image/upload/e_blur:300/menu/items/osh.jpg
```

### 3. CDN

Rasmlar global CDN orqali serve qilinadi:
- ✅ Tez yuklash
- ✅ Har qanday joydan
- ✅ Avtomatik caching

---

## 🔒 Xavfsizlik

### API Keys ni Himoya Qilish

1. ❌ **Git ga commit qilmang**:
```bash
# .gitignore da
.env
```

2. ✅ **Environment variables ishlatish**:
```python
CLOUDINARY_API_SECRET = os.getenv('CLOUDINARY_API_SECRET')
```

3. ✅ **Railway Variables**:
   - Faqat Railway da ko'rinadi
   - Git history da yo'q

---

## 📋 Troubleshooting

### 1. Rasmlar Yuklanmayapti

**Xato**: `cloudinary.exceptions.Error: Must supply api_key`

**Yechim**:
1. `.env` faylda `USE_CLOUDINARY=True` borligini tekshiring
2. `CLOUDINARY_CLOUD_NAME`, `API_KEY`, `API_SECRET` to'g'ri yozilganini tekshiring
3. Server ni qayta ishga tushiring

### 2. Railway da Rasmlar Ko'rinmayapti

**Yechim**:
1. Railway Variables da Cloudinary credentials borligini tekshiring
2. `USE_CLOUDINARY=True` o'rnatilganini tekshiring
3. Redeploy qiling

### 3. Invalid Cloud Name

**Xato**: `cloudinary.exceptions.Error: Invalid cloud_name`

**Yechim**:
1. Cloudinary dashboard → Account Details
2. Cloud name ni nusxa oling (to'g'ri yozing!)
3. Railway Variables ni yangilang

---

## 💰 Narxlar

### Free Plan (Boshlanish uchun)

- ✅ 25 GB storage
- ✅ 25 GB bandwidth/month
- ✅ 25,000 transformations/month
- ✅ Unlimited images
- ✅ CDN

**Bu ko'p restoran uchun yetarli!**

### Paid Plans (Katta loyihalar uchun)

- **Plus**: $99/month - 100 GB storage
- **Advanced**: $249/month - 250 GB storage
- **Custom**: Aloqa qiling

---

## 🎯 Best Practices

### 1. Rasm Formatlar

✅ **Tavsiya etiladi**:
- JPEG: Fotografiyalar uchun
- PNG: Logo, icon uchun
- WebP: Avtomatik (Cloudinary konvertatsiya qiladi)

### 2. Rasm O'lchamlari

✅ **Tavsiya**:
- Menu items: 800x600px
- Thumbnails: 300x300px
- Logo: 200x200px

### 3. Folder Structure

Cloudinary da folder yaratish:

```python
# models.py da
image_url = models.ImageField(upload_to='menu/items/')
```

Natija:
```
menu/
  items/
    osh.jpg
    lagmon.jpg
  categories/
    asosiy-taomlar.jpg
```

---

## ✅ Checklist

Deploy qilishdan oldin:

- [ ] Cloudinary account yaratildi
- [ ] Cloud name, API key, API secret olindi
- [ ] Local `.env` faylda Cloudinary credentials qo'shildi
- [ ] `USE_CLOUDINARY=True` o'rnatildi
- [ ] Local da test qilindi (rasm yuklandi)
- [ ] Railway Variables da Cloudinary credentials qo'shildi
- [ ] Git push qilindi
- [ ] Railway da test qilindi

---

## 🎉 Natija

Endi rasmlar:
- ✅ Cloudinary da saqlanadi
- ✅ Hech qachon o'chib ketmaydi
- ✅ Tez yuklash (CDN)
- ✅ Avtomatik optimizatsiya
- ✅ Railway bilan mukammal ishlaydi

**Rasm URL misol**:
```
https://res.cloudinary.com/dastyormenu/image/upload/v1234567890/menu/items/osh.jpg
```

---

## 📞 Keyingi Qadamlar

1. **Cloudinary account yarating**: https://cloudinary.com
2. **Credentials oling**: Dashboard → Account Details
3. **Local `.env` yangilang**
4. **Test qiling**: Rasm yuklang
5. **Railway Variables qo'shing**
6. **Deploy qiling**: `git push origin main`

Omad! 🚀
