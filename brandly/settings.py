from pathlib import Path
import os
from dotenv import load_dotenv  # ← ekledik
from corsheaders.defaults import default_headers

# .env dosyasını yükle
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SERPER_API_KEY = os.getenv("SERPER_API_KEY")

# Güvenlik Ayarları
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "unsafe-default")
DEBUG = os.getenv("DEBUG", "False") == "True"

ALLOWED_HOSTS = [
    "yonet.siteadi.com",
    "localhost",
    "127.0.0.1",
    "45.84.191.180",
]

# Statik Dosyalar
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Medya Dosyaları
MEDIA_URL = '/output_files/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'output_files')

# Uygulamalar
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'kullanici',
    'analiz',
]

# Middleware
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# CORS Ayarları
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://siteadi.com",
    "https://www.siteadi.com"
]

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = list(default_headers) + ['content-disposition']
CORS_EXPOSE_HEADERS = ['Content-Disposition']

# URL Ayarları
ROOT_URLCONF = 'brandly.urls'

# Template
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'brandly.wsgi.application'

# Veritabanı
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Şifre Doğrulayıcılar
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Uluslararası Ayarlar
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# REST framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
}


# Custom User Model
AUTH_USER_MODEL = 'kullanici.CustomUser'

# CSRF için güvenilir originler
CSRF_TRUSTED_ORIGINS = [
    "https://yonet.siteadi.com",
    "https://siteadi.com",
    "https://www.siteadi.com"
]
