# 📸 Railway Media Files (Rasmlar) - Hal Qilish

## ❌ Muammo

Railway da yuklangan rasmlar ochilmayapti:

```
http://dastyormenu-backend-production.up.railway.app/media/menu/items/8.png
```

**Sabab**: Railway **ephemeral filesystem** ishlatadi - har deploy qilganda fayllar o'chib ketadi!

---

## ✅ Yechim 1: Django Static Serve (Vaqtinchalik)

### O'zgarishlar

**1. `config/urls.py`** - Media fayllarni serve qilish:

```python
from django.views.static import serve
from django.urls import re_path

# Production da media fayllarni serve qilish
if not settings.DEBUG:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]
```

**2. `config/settings/production.py`** - WhiteNoise sozlamalari:

```python
WHITENOISE_AUTOREFRESH = True
WHITENOISE_USE_FINDERS = True
WHITENOISE_MIMETYPES = {
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.png': 'image/png',
    '.gif': 'image/gif',
    '.webp': 'image/webp',
}
```

### ⚠️ Ogohlantirish

**Bu yechim vaqtinchalik!** Har deploy qilganda fayllar o'chib ketadi.

---

## ✅ Yechim 2: AWS S3 / Cloudinary (Production uchun - TAVSIYA)

### AWS S3 Setup

#### 1. AWS S3 Bucket Yaratish

1. AWS Console → S3 → Create bucket
2. Bucket name: `dastyormenu-media`
3. Region: `us-east-1` (yoki yaqin region)
4. Block all public access: **OFF** (rasmlar public bo'lishi kerak)
5. Create bucket

#### 2. IAM User Yaratish

1. AWS Console → IAM → Users → Add user
2. User name: `dastyormenu-s3-user`
3. Access type: **Programmatic access**
4. Permissions: **AmazonS3FullAccess**
5. Save **Access Key ID** va **Secret Access Key**

#### 3. Bucket Policy

S3 bucket → Permissions → Bucket Policy:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::dastyormenu-media/*"
    }
  ]
}
```

#### 4. CORS Configuration

S3 bucket → Permissions → CORS:

```json
[
  {
    "AllowedHeaders": ["*"],
    "AllowedMethods": ["GET", "PUT", "POST", "DELETE"],
    "AllowedOrigins": ["*"],
    "ExposeHeaders": []
  }
]
```

#### 5. Railway Variables

Railway → Variables → Add:

```bash
USE_S3=True
AWS_ACCESS_KEY_ID=your_access_key_id
AWS_SECRET_ACCESS_KEY=your_secret_access_key
AWS_STORAGE_BUCKET_NAME=dastyormenu-media
AWS_S3_REGION_NAME=us-east-1
```

#### 6. Requirements

`requirements.txt` da allaqachon bor:

```txt
django-storages==1.14.2
boto3==1.34.84
```

#### 7. Settings

`config/settings/base.py` da allaqachon sozlangan:

```python
USE_S3 = os.getenv('USE_S3', 'False') == 'True'
if USE_S3:
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME', 'us-east-1')
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
    AWS_DEFAULT_ACL = 'public-read'
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
```

---

## ✅ Yechim 3: Cloudinary (Oson va Bepul)

### Cloudinary Setup

#### 1. Account Yaratish

1. https://cloudinary.com → Sign Up
2. Free plan: 25GB storage, 25GB bandwidth/month

#### 2. Credentials Olish

Dashboard → Account Details:
- Cloud name: `your_cloud_name`
- API Key: `your_api_key`
- API Secret: `your_api_secret`

#### 3. Package O'rnatish

```bash
pip install cloudinary django-cloudinary-storage
```

`requirements.txt` ga qo'shing:

```txt
cloudinary==1.36.0
django-cloudinary-storage==0.3.0
```

#### 4. Settings

`config/settings/base.py` ga qo'shing:

```python
# Cloudinary
USE_CLOUDINARY = os.getenv('USE_CLOUDINARY', 'False') == 'True'
if USE_CLOUDINARY:
    INSTALLED_APPS += ['cloudinary_storage', 'cloudinary']
    
    CLOUDINARY_STORAGE = {
        'CLOUD_NAME': os.getenv('CLOUDINARY_CLOUD_NAME'),
        'API_KEY': os.getenv('CLOUDINARY_API_KEY'),
        'API_SECRET': os.getenv('CLOUDINARY_API_SECRET'),
    }
    
    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
```

#### 5. Railway Variables

```bash
USE_CLOUDINARY=True
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```

---

## 📊 Yechimlar Taqqoslash

| Yechim | Narx | Osonlik | Ishonchlilik | Tavsiya |
|--------|------|---------|--------------|---------|
| Django Static Serve | Bepul | ⭐⭐⭐⭐⭐ | ⭐ | ❌ Faqat test uchun |
| AWS S3 | ~$0.023/GB | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ✅ Production |
| Cloudinary | Bepul (25GB) | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ✅ Boshlang'ich |

---

## 🚀 Deploy Qilish

### Yechim 1 (Vaqtinchalik)

```bash
git add .
git commit -m "Added media file serving for Railway"
git push origin main
```

**Eslatma**: Har deploy qilganda rasmlar o'chib ketadi!

### Yechim 2 (S3)

1. AWS S3 sozlang
2. Railway Variables qo'shing
3. Deploy qiling:

```bash
git push origin main
```

### Yechim 3 (Cloudinary)

1. Cloudinary account yarating
2. Package qo'shing: `pip install cloudinary django-cloudinary-storage`
3. Settings yangilang
4. Railway Variables qo'shing
5. Deploy qiling

---

## 🧪 Test Qilish

### Local

```bash
# Server ishga tushiring
python manage.py runserver

# Rasm yuklang (admin panel yoki API orqali)
# Rasm URL ni tekshiring
curl http://localhost:8000/media/menu/items/test.jpg
```

### Railway

```bash
# Rasm URL ni tekshiring
curl https://dastyormenu-backend-production.up.railway.app/media/menu/items/test.jpg
```

**S3 bilan**:
```
https://dastyormenu-media.s3.amazonaws.com/menu/items/test.jpg
```

**Cloudinary bilan**:
```
https://res.cloudinary.com/your_cloud_name/image/upload/menu/items/test.jpg
```

---

## 💡 Tavsiyalar

### Test Uchun (Hozir)

✅ **Django Static Serve** ishlatish mumkin (Yechim 1)
- Tez va oson
- Fayllar o'chib ketadi (har deploy da)
- Faqat test uchun

### Production Uchun (Keyinchalik)

✅ **Cloudinary** - Eng oson va bepul (25GB)
✅ **AWS S3** - Professional, ishonchli

---

## 🔧 Hozirgi Holat

**O'zgarishlar qilindi**:
1. ✅ `config/urls.py` - Media serve qo'shildi
2. ✅ `config/settings/production.py` - WhiteNoise sozlandi

**Keyingi qadam**:
```bash
git add .
git commit -m "Added media file serving for Railway"
git push origin main
```

**Eslatma**: Bu vaqtinchalik yechim! Production uchun S3 yoki Cloudinary ishlatish kerak.

---

Omad! 🚀
