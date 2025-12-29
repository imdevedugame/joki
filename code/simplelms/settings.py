"""
Django settings for simplelms project.
Konfigurasi untuk Docker + Bahasa Indonesia + Zona Waktu Asia/Jakarta.
"""

from pathlib import Path
import os

# --- PATH DASAR PROJECT ---
BASE_DIR = Path(__file__).resolve().parent.parent

# --- KEAMANAN ---
SECRET_KEY = 'django-insecure-@9akp-k7lwjzm2=%wf(e_@h%5o4g#zfch2hyu2jb9guc)2np*7'
DEBUG = True
ALLOWED_HOSTS = ['*']  # agar bisa diakses dari Docker / localhost

# --- APLIKASI YANG DIGUNAKAN ---
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',          # aplikasi utama
    'silk',          # untuk profiling query
    "ninja_simple_jwt"
]

# --- MIDDLEWARE ---
MIDDLEWARE = [
    'silk.middleware.SilkyMiddleware',  # wajib di paling atas untuk profiling
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# --- URL & TEMPLATE ---
ROOT_URLCONF = 'simplelms.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'core' / 'templates'],  # folder template core
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'simplelms.wsgi.application'

# --- DATABASE ---
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'simple_lms',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'simple_db',  # nama service di docker-compose
        'PORT': '5432',
    }
}

# --- VALIDASI PASSWORD ---
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# --- BAHASA & ZONA WAKTU ---
LANGUAGE_CODE = 'id'
TIME_ZONE = 'Asia/Jakarta'
USE_I18N = True
USE_TZ = True

# --- FILE STATIS ---
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# --- ID OTOMATIS DEFAULT ---
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --- KONFIGURASI SILK (Profiling ORM) ---
SILKY_PYTHON_PROFILER = True
SILKY_INTERCEPT_PERCENT = 100  # memantau semua request
SILKY_MAX_REQUEST_BODY_SIZE = -1
SILKY_MAX_RESPONSE_BODY_SIZE = -1
SILKY_META = True

# --- LOCAL SETTINGS OPSIONAL ---
try:
    from simplelms.local_settings import *
except ImportError:
    pass
