import os
import dj_database_url
from pathlib import Path

# 1. Django ki default line pehle se likhi hogi:
BASE_DIR = Path(__file__).resolve().parent.parent

# 🎯 FIX: Jo do lines upar galat jagah thi, unhe BAS IS BASE_DIR KE NEECHE paste kar do!
import environ
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))



SECRET_KEY = 'django-insecure-u3nt!fe4lgyrq%$xdu=ac-j**#2$3v!33di3z)bd8c4dygm0v+'

DEBUG = True

ALLOWED_HOSTS = ['*']

# --- YAHAN DEKH, YE ZAROORI HAI ---
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',  # <--- Ye line add kar
    'rest_framework',
    'crm',
    
]
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # <--- Ise yahan ekdum sahi jagah par daal
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'core.wsgi.application'

DATABASES = {
    'default': dj_database_url.config(
        default='postgres://postgres:flight123@localhost:5432/skybook_db',
        conn_max_age=600,
        ssl_require=True
    )
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# --- CORS CONFIGURATION ---
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5174",
    # Yahan apne live frontend ka URL daalna, example:
    "https://your-frontend-project.vercel.app", 
]
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
CORS_ALLOW_CREDENTIALS = True
STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --- EMAIL SETTINGS ---

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'mail.a.hostedemail.com'

# 🎯 Secure Port configuration for Business Mail
EMAIL_PORT = 465                   # <-- 587 se badal kar 465 kiya (SSL ke liye)
EMAIL_USE_TLS = False              # <-- TLS band kiya
EMAIL_USE_SSL = True               # <-- SSL chalu kiya
EMAIL_TIMEOUT = 20

EMAIL_HOST_USER = 'support@roamifyllc.com' 
EMAIL_HOST_PASSWORD = 'Bholenath@108'  # <-- Tera password bilkul sahi hai yahan

DEFAULT_FROM_EMAIL = 'Roamify Support <support@roamifyllc.com>'
EMAIL_FAIL_SILENTLY = False