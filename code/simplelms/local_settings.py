# local_settings.py
# File ini digunakan untuk override pengaturan di settings.py
# Khusus untuk konfigurasi lokal (misalnya database, debug mode, dsb.)

DEBUG = True

ALLOWED_HOSTS = ['*']  # supaya bisa diakses dari browser lokal maupun container

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'simple_lms',       # nama database dari docker-compose
        'USER': 'postgres',         # username dari docker-compose
        'PASSWORD': 'postgres',     # password dari docker-compose
        'HOST': 'simple_db',        # nama service postgres di docker-compose
        'PORT': '5432',             # port default PostgreSQL
    }
}

# Zona waktu lokal Indonesia
TIME_ZONE = 'Asia/Jakarta'
USE_TZ = True
