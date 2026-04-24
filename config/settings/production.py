"""Production settings."""
import os
from .base import *

DEBUG = os.getenv('DEBUG', 'False') == 'True'

# ALLOWED_HOSTS - Railway uchun
allowed_hosts = os.getenv('ALLOWED_HOSTS', '')
if allowed_hosts:
    ALLOWED_HOSTS = [host.strip() for host in allowed_hosts.split(',') if host.strip()]
else:
    # Default Railway pattern
    ALLOWED_HOSTS = ['*']  # Faqat test uchun, production da aniq domain kiriting!

# CORS
INSTALLED_APPS += ['corsheaders']
MIDDLEWARE.insert(2, 'corsheaders.middleware.CorsMiddleware')

# CORS Settings
cors_origins = os.getenv('CORS_ALLOWED_ORIGINS', '').split(',') if os.getenv('CORS_ALLOWED_ORIGINS') else []
if cors_origins and cors_origins[0]:
    CORS_ALLOWED_ORIGINS = [origin.strip() for origin in cors_origins if origin.strip()]
else:
    CORS_ALLOWED_ORIGINS = []
CORS_ALLOW_CREDENTIALS = True

# CSRF Settings - MUHIM!
csrf_origins = os.getenv('CSRF_TRUSTED_ORIGINS', '').split(',') if os.getenv('CSRF_TRUSTED_ORIGINS') else []
if csrf_origins and csrf_origins[0]:
    CSRF_TRUSTED_ORIGINS = [origin.strip() for origin in csrf_origins if origin.strip()]
else:
    # Default: ALLOWED_HOSTS dan olish (faqat * bo'lmasa)
    if ALLOWED_HOSTS and ALLOWED_HOSTS != ['*']:
        CSRF_TRUSTED_ORIGINS = [f'https://{host}' for host in ALLOWED_HOSTS if host != '*' and not host.startswith('.')]
    else:
        CSRF_TRUSTED_ORIGINS = []

# Static files with WhiteNoise
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Security Settings - Railway uchun optimallashtirilgan
SECURE_SSL_REDIRECT = False  # Railway o'zi HTTPS ni boshqaradi
SESSION_COOKIE_SECURE = False  # Railway proxy orqali
CSRF_COOKIE_SECURE = False  # Railway proxy orqali
CSRF_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_HTTPONLY = False
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'SAMEORIGIN'

# S3 Storage (optional)
USE_S3 = os.getenv('USE_S3', 'False') == 'True'
