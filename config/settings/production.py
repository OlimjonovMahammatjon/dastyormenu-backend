"""Production settings."""
import os
from .base import *

DEBUG = os.getenv('DEBUG', 'False') == 'True'

# CORS
INSTALLED_APPS += ['corsheaders']
MIDDLEWARE.insert(2, 'corsheaders.middleware.CorsMiddleware')

# CORS Settings
CORS_ALLOWED_ORIGINS = os.getenv('CORS_ALLOWED_ORIGINS', '').split(',') if os.getenv('CORS_ALLOWED_ORIGINS') else []
CORS_ALLOW_CREDENTIALS = True

# CSRF Settings - Railway domain qo'shish
csrf_origins = os.getenv('CSRF_TRUSTED_ORIGINS', '').split(',') if os.getenv('CSRF_TRUSTED_ORIGINS') else []
# Railway domain avtomatik qo'shish
if not csrf_origins:
    csrf_origins = []
# Railway.app domainlarini qo'shish
railway_domain = os.getenv('RAILWAY_PUBLIC_DOMAIN')
if railway_domain:
    csrf_origins.append(f'https://{railway_domain}')
# .railway.app wildcard
csrf_origins.append('https://*.railway.app')
CSRF_TRUSTED_ORIGINS = csrf_origins

# Static files with WhiteNoise
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Security
SECURE_SSL_REDIRECT = os.getenv('SECURE_SSL_REDIRECT', 'True') == 'True'
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_SAMESITE = 'Lax'
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'SAMEORIGIN'  # Admin panel uchun
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# S3 Storage (optional)
USE_S3 = os.getenv('USE_S3', 'False') == 'True'
